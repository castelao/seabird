#!/usr/bin/env python

""" Export the parsed data into a NetCDF following different patterns
"""

from __future__ import print_function
from datetime import datetime, date, time
import logging

module_logger = logging.getLogger("seabird.netcdf")

try:
    import netCDF4
except:
    module_logger.warning("netCDF4 is not available.")


def get_cf_attributes(attrs):
    if "longname" in attrs:
        attrs["long_name"] = attrs.pop("longname")
    value_min = attrs.pop("valuemin") if "valuemin" in attrs else None
    value_max = attrs.pop("valuemax") if "valuemax" in attrs else None
    if value_min and value_max:
        attrs["actual_range"] = (value_min, value_max)
    return attrs


def cnv2nc(data, filename):
    """Save a CNV() object into filename as a NetCDF

    To save the CTD.cnv into a NetCDF, just run:

    profile = cnv.fCNV("CTD.cnv")
    cnv2nc(profile, "CTD.nc")
    """
    logging.info("Saving netcdf output file: %s" % filename)

    nc = netCDF4.Dataset(filename, "w", format="NETCDF4")

    nc.history = "Created by cnv2nc (PyCNV)"

    nc.date_created = datetime.now().isoformat()

    # print "Global attributes"
    A = sorted(data.attrs.keys())
    for a in A:
        try:
            if type(data.attrs[a]) is datetime:
                nc.__setattr__(a, data.attrs[a].isoformat())
            else:
                nc.__setattr__(a, data.attrs[a])
        except:
            module_logger.warning("Failed to write global attribute %s" % a)

    real_values = len(data[data.keys()[0]])
    if "nvalue" not in data.attributes:
        logging.warning(
            "Unknown original data length, nvalues not available within the cnv file."
        )
    elif real_values != int(data.attributes["nvalues"]):
        logging.warning(
            "\033[91mATENTION '%s' records available differ from nvalues='%s'."
            % (real_values, data.attributes["nvalues"])
        )
    nc.createDimension("scan", len(data[data.keys()[0]]))

    logging.info("Variabes")
    cdf_variables = {}
    for name in data.keys():
        logging.info(name)
        var = data[name]

        # If duplicate consider first variable only
        if name in cdf_variables:
            logging.warning(
                "\033[91mATENTION The duplicated variables are not compatible with the NetCDF Format. "
                + "Only the very first variable '%s' will be considered." % name
            )
            continue

        # Rename Variable if bad character
        if "/" in name:
            nc_name = name.replace("/", "Per")
            logging.info(
                "Replace {} in variable by {} to be compatible with NetCDF".format(
                    name, nc_name
                )
            )
        else:
            nc_name = name

        # Add variable to dataset
        # handle datetime variables, convert to string format
        if var.dtype == object and type(var[0]) in (datetime, time, date):
            str_data = var.data.astype(str)
            cdf_variables[nc_name] = nc.createVariable(
                nc_name, "S%g" % len(str_data[0]), ("scan",)
            )
            cdf_variables[nc_name][:] = str_data
        else:
            cdf_variables[nc_name] = nc.createVariable(nc_name, var.dtype, ("scan",))
            cdf_variables[nc_name][:] = var.data

        # Ignore unknown fill_value
        if var.fill_value not in ("?", "N/A"):
            cdf_variables[nc_name].missing_value = var.fill_value

        # Add Attributes
        for key, value in get_cf_attributes(var.attrs).items():
            # Ignore name and empty attributes
            if key in ["name"] or value == None:
                continue
            logging.info("\t\033[93m{}\033[0m: {}".format(key, value))
            cdf_variables[nc_name].__setattr__(key, value)

    nc.close()
