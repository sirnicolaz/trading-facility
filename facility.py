import argparse
import start_cui, start_monitor, start_tracker, start_proxy


parser = argparse.ArgumentParser(description='Trading facility.')
subparsers = parser.add_subparsers(dest='command')

parser_bot = subparsers.add_parser('bot', help="runs a bot")
subparsers_bot = parser_bot.add_subparsers(dest='action')
parser_take_profit = subparsers_bot.add_parser('take_profit')
parser_take_profit.add_argument('coin', action='store_true', help="the currency")
parser_take_profit.add_argument('win', action='store_true', help="the %% win to sell")

parser_cui = subparsers.add_parser('cui', help="runs a console user interface")
subparsers_cui = parser_cui.add_subparsers(dest='type')
parser_monitor = subparsers_cui.add_parser('monitor', help="currency analysis monitor")
parser_monitor = subparsers_cui.add_parser('trading', help="trading dashboard")

parser_tracker = subparsers.add_parser('tracker', help="runs ta trackers")
supported_indicators = ["rsi", "macd_trend", "adx_trend"]
parser_tracker.add_argument('--indicators', '-i', type=str, nargs="*", choices=supported_indicators)

parser_proxy = subparsers.add_parser('proxy', help="runs the bittrex proxy (to support conditional orders.")
parser_proxy.add_argument('--cookies-file', '-c', type=str, help="path to the authenticated cookies file")

args = parser.parse_args()

if args.command == "cui":
    {
        "monitor": start_monitor,
        "cui": start_cui
    }[args.type].run()
elif args.command == "tracker":
    trackers = args.indicators if args.indicators else supported_indicators
    start_tracker.run(trackers)
elif args.command == "proxy":
    start_proxy.run(args.cookies_file)
else:
    parser.print_usage()