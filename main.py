import argparse

from pipeline.orchestrator import run_pipeline


def main():
    arg_parser = argparse.ArgumentParser(
        description="Rank Letterboxd watchlist films by taste similarity."
    )

    arg_parser.add_argument(
        "-u",
        "--username",
        type=str,
        default="",
        metavar="USERNAME",
        help="Letterboxd username",
        required=True,
    )

    arg_parser.add_argument(
        "-n",
        "--top-n",
        type=int,
        default=10,
        metavar="N",
        help="number of top-ranked watchlist films to output (default: 10)",
    )

    args = arg_parser.parse_args()

    if args.top_n < 1:
        arg_parser.error("--top-n must be at least 1")

    run_pipeline(args.username, top_n=args.top_n)


if __name__ == "__main__":
    main()
