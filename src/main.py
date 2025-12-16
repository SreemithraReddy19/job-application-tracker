import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Job Application Tracker CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # -------- add command --------
    add_parser = subparsers.add_parser(
        "add", help="Add a new job application"
    )
    add_parser.add_argument("--company", required=True)
    add_parser.add_argument("--role", required=True)
    add_parser.add_argument("--location")
    add_parser.add_argument("--source")
    add_parser.add_argument("--notes")

    # -------- list command --------
    list_parser = subparsers.add_parser(
        "list", help="List job applications"
    )
    list_parser.add_argument("--company")
    list_parser.add_argument("--status")

    # -------- update command --------
    update_parser = subparsers.add_parser(
        "update", help="Update a job application"
    )
    update_parser.add_argument("--company", required=True)
    update_parser.add_argument("--role")
    update_parser.add_argument("--status")
    update_parser.add_argument("--notes")

    args = parser.parse_args()

    # Day 2 deliverable: just print parsed args
    print("Parsed arguments:")
    print(args)


if __name__ == "__main__":
    main()
