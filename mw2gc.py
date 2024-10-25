#!/usr/bin/env python3

import argparse
from pathlib import Path

from fit_tool.fit_file import FitFile
from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.file_creator_message import FileCreatorMessage
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.lap_message import LapMessage
from fit_tool.profile.messages.record_message import (
    RecordMessage,
    RecordTemperatureField,
)
from fit_tool.profile.messages.session_message import SessionMessage

parser = argparse.ArgumentParser(
    prog="mw2gc.py",
    description="Improve MyWhoosh activity files for Garmin Connect uplaod",
)

parser.add_argument(
    "-d", "--debug", help="write .csv files for comparision", action="store_true"
)
parser.add_argument("filename")
args = parser.parse_args()

in_file = FitFile.from_file(args.filename)

if args.debug:
    in_file.to_csv(f"{Path(args.filename).stem}.in.csv")

builder = FitFileBuilder()

cadence_values = []
power_values = []
heart_rate_values = []

for record in in_file.records:
    message = record.message

    if isinstance(message, FileCreatorMessage):
        ## remove wrong device information
        continue

    if isinstance(message, FileIdMessage):
        pass

    if isinstance(message, LapMessage):
        ## remove wrong interval information
        continue

    if isinstance(message, RecordMessage):
        ## remove wrong temperature information
        message.remove_field(RecordTemperatureField.ID)

        cadence_values.append(message.cadence if message.cadence else 0)
        power_values.append(message.power if message.power else 0)
        heart_rate_values.append(message.heart_rate if message.heart_rate else 0)

    if isinstance(message, SessionMessage):
        ## add missing average values
        if not message.avg_cadence:
            message.avg_cadence = sum(cadence_values) / len(cadence_values)
        if not message.avg_power:
            message.avg_power = sum(power_values) / len(power_values)
        if not message.avg_heart_rate:
            message.avg_heart_rate = sum(heart_rate_values) / len(heart_rate_values)

        cadence_values = []
        power_values = []
        heart_rate_values = []

    builder.add(message)

## output .fit file
out_file = builder.build()
out_file.to_file(f"{Path(args.filename).stem}.fit")

if args.debug:
    out_file.to_csv(f"{Path(args.filename).stem}.out.csv")
