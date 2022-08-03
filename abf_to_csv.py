import pyabf
import pandas as pd
from glob import glob
import argparse
import re

def abf_to_df(
    filename:str,
    current_channel:int = 0,
    voltage_channel:int = 1,
    barrel_channel:int = 3
    ):
    abf = pyabf.ABF(filename)

    time = []
    recordings = {
        'Current': [],
        'Voltage': [],
        'Barrel': []
    }
    current_label = None
    voltage_label = None

    for sweep in abf.sweepList:
        try:
            abf.setSweep(sweep, channel = current_channel)
            time.extend(abf.sweepX)
            recordings['Current'].extend(abf.sweepY)
            current_label = abf.sweepLabelY
        except ValueError:
            print(f'Warning: failed to access given channel for current in {filename}, sweep {sweep}')
        try:
            abf.setSweep(sweep, channel = voltage_channel)
            recordings['Voltage'].extend(abf.sweepY)
            voltage_label = abf.sweepLabelY
        except ValueError:
            print(f'Warning: failed to access given channel for voltage in {filename}, sweep {sweep}')
        try:
            abf.setSweep(sweep, channel = barrel_channel)
            recordings['Barrel'].extend(abf.sweepY)
        except ValueError:
            print(f'Warning: failed to access given channel for barrel in {filename}, sweep {sweep}')



    df = pd.DataFrame({
        'Time': time
    })

    for channel, values in recordings.items():
        if len(values) == len(df.Time):
            df[channel] = values

    df['Voltage_Label'] = re.search('\((.{2})\)', voltage_label).group(1)
    df['Current_Label'] = re.search('\((.{2})\)', current_label).group(1)
    df['Filename'] = filename

    return df

def main(args):
    input_abfs = glob(args.input)
    parsed_abfs = [abf_to_df(
        abf,
        args.current_channel,
        args.voltage_channel,
        args.barrel_channel
    ) for abf in input_abfs]

    combined_abfs = pd.concat(parsed_abfs)
    combined_abfs.to_csv(args.output, index = False)

parser = argparse.ArgumentParser(
    description = 'Convert ABFs to CSV'
)
parser.add_argument(
    'input',
    help = 'Input abf files. Can be a glob, like "*.abf"',
)
parser.add_argument(
    '-o',
    '--output',
    help = 'Output csv file. Default "combined_traces.csv"',
    default = 'combined_traces.csv'
)
parser.add_argument(
    '-i',
    '--current-channel',
    help = 'Channel to which current is recorded. Default 0.',
    type = int,
    default = 0
)
parser.add_argument(
    '-v',
    '--voltage_channel',
    help = 'Channel to which voltage is recorded. Default 1.',
    type = int,
    default = 1
)
parser.add_argument(
    '-b',
    '--barrel-channel',
    help = 'Channel to which barrel position is recorded. Default 3.',
    type = int,
    default = 3
)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)