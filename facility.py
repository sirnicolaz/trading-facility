import argparse
import start_cui, start_monitor

parser = argparse.ArgumentParser(description='Trading facility.')
subparsers = parser.add_subparsers(dest='command')

parser_bot = subparsers.add_parser('bot', help="runs a bot")
subparsers_bot = parser_bot.add_subparsers(dest='action')
parser_take_profit = subparsers_bot.add_parser('take_profit')
parser_take_profit.add_argument('coin', action='store_true', help="the currency")
parser_take_profit.add_argument('win', action='store_true', help="the %% win to sell")


#parser_bot.add_argument('--action', action = 'store_true',
#                        choices=["take_profit", "stop_loss", "chandelier_exit_dynamic_stop_loss"])

parser_cui = subparsers.add_parser('cui', help="runs a console user interface")
subparsers_cui = parser_cui.add_subparsers(dest='type')
parser_monitor = subparsers_cui.add_parser('monitor', help="currency analysis monitor")
parser_monitor = subparsers_cui.add_parser('trading', help="trading dashboard")

#bot_parser = argparse.ArgumentParser(parents=[parser])
#bot_parser.add_argument('--action', '-a', metavar="dio", type=str, nargs=1, help="which bot you want to run?",
#                        choices=["take_profit", "stop_loss", "chandelier_exit_dynamic_stop_loss"])
#bot_parser.parse_args()
#parser.print_help()
args = parser.parse_args()

if args.command == "cui":
    {
        "monitor": start_monitor,
        "cui": start_cui
    }[args.type].run()
