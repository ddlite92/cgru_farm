#!/usr/bin/env python3
"""List shot names from afserver jobs that carry a specific ticket/need_properties value.

Connects to the Afanasy server, fetches all jobs, and filters those whose
job-level need_properties field contains the requested ticket string.  Also
checks block-level tickets dicts in case the job uses the ticket system
instead.  Prints only the shot name (e.g. sh062a) extracted from each
matching job name, sorted and deduplicated.

Usage:
    python3 list_highspec_shots.py [options]

Options:
    --server SERVER     afserver hostname or IP  (default: 192.168.90.104)
    --port   PORT       afserver TCP port        (default: 51000)
    --ticket TICKET     need_properties / ticket name to filter on
                        (default: highspec)
    --verbose           Print full job name and state alongside shot name

Examples:
    python3 list_highspec_shots.py --verbose
    python3 list_highspec_shots.py --ticket BM3 --server 192.168.90.103
"""

import argparse
import re
import sys

import cgruconfig
import af


DEFAULT_SERVER_ADDRESS = "192.168.90.104"
DEFAULT_SERVER_PORT = 51000
DEFAULT_TICKET_NAME = "highspec"

SHOT_NAME_PATTERN = re.compile(r"sh\w+")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed argument namespace with server, port, ticket, and verbose fields.
    """
    parser = argparse.ArgumentParser(
        description=(
            "List shot names from afserver jobs that carry a specific "
            "ticket or need_properties value."
        )
    )
    parser.add_argument(
        "--server",
        default=DEFAULT_SERVER_ADDRESS,
        help=f"afserver hostname or IP (default: {DEFAULT_SERVER_ADDRESS})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_SERVER_PORT,
        help=f"afserver TCP port (default: {DEFAULT_SERVER_PORT})",
    )
    parser.add_argument(
        "--ticket",
        default=DEFAULT_TICKET_NAME,
        help=f"need_properties value or ticket name to filter on (default: {DEFAULT_TICKET_NAME})",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print full job name and state alongside the shot name.",
    )
    return parser.parse_args()


def configure_server(server_address: str, server_port: int) -> None:
    """Override afserver connection parameters in cgruconfig before af.Cmd() is created.

    Args:
        server_address: Hostname or IP of the afserver.
        server_port: TCP port the afserver listens on.
    """
    cgruconfig.VARS["af_servername"] = server_address
    cgruconfig.VARS["af_serverport"] = server_port


def fetch_all_jobs(cmd: af.Cmd, verbose: bool) -> list:
    """Retrieve the complete job list from afserver.

    Args:
        cmd: An initialised af.Cmd instance.
        verbose: Forward verbosity flag to the network layer.

    Returns:
        List of raw job dicts from the server.

    Raises:
        RuntimeError: If the server returns no data.
    """
    job_list = cmd.getJobList(verbose=verbose)
    if job_list is None:
        raise RuntimeError(
            "afserver returned no data — is afserver running and reachable?"
        )
    return job_list


def job_has_ticket(job: dict, ticket_name: str) -> bool:
    """Return True if the job carries the requested ticket or need_properties value.

    Checks two locations:
    - Job-level need_properties (substring match, case-insensitive)
    - Block-level tickets dict keys (present only when a ticket is set)

    Args:
        job: Raw job dict from the server.
        ticket_name: The ticket/need_properties string to look for.

    Returns:
        True if the job matches, False otherwise.
    """
    normalised_ticket = ticket_name.lower()

    job_need_properties = job.get("need_properties", "")
    if normalised_ticket in job_need_properties.lower():
        return True

    for block in job.get("blocks", []):
        block_tickets = block.get("tickets")
        if isinstance(block_tickets, dict):
            if any(normalised_ticket in key.lower() for key in block_tickets):
                return True

    return False


def extract_shot_name(job_name: str) -> str:
    """Extract the shot identifier (shXXX) from a job name.

    Args:
        job_name: Full Afanasy job name string.

    Returns:
        The shot token (e.g. 'sh062a') if found, otherwise the full job name.
    """
    match = SHOT_NAME_PATTERN.search(job_name)
    return match.group(0) if match else job_name


def main() -> int:
    """Fetch jobs and print shot names for those matching the ticket filter.

    Returns:
        Exit code: 0 on success, 1 on error or no matches.
    """
    args = parse_args()

    configure_server(args.server, args.port)

    if args.verbose:
        print(
            f"Connecting to afserver at [IP_REDACTED]:{args.port} ...",
            file=sys.stderr,
        )

    cmd = af.Cmd()

    try:
        all_jobs = fetch_all_jobs(cmd, verbose=False)
    except RuntimeError as fetch_error:
        print(f"ERROR: {fetch_error}", file=sys.stderr)
        return 1

    matching_jobs = [j for j in all_jobs if job_has_ticket(j, args.ticket)]

    if not matching_jobs:
        print(
            f"No jobs found with ticket/need_properties '{args.ticket}'.",
            file=sys.stderr,
        )
        return 1

    seen_shots = set()
    ordered_shots = []
    shot_to_jobs: dict[str, list] = {}

    for job in matching_jobs:
        job_name = job.get("name", "")
        shot_name = extract_shot_name(job_name)

        if shot_name not in seen_shots:
            seen_shots.add(shot_name)
            ordered_shots.append(shot_name)
            shot_to_jobs[shot_name] = []

        shot_to_jobs[shot_name].append(job)

    ordered_shots.sort()

    if args.verbose:
        print(
            f"\n{len(matching_jobs)} job(s) / {len(ordered_shots)} unique shot(s) "
            f"with ticket '{args.ticket}':\n",
            file=sys.stderr,
        )
        for shot_name in ordered_shots:
            for job in shot_to_jobs[shot_name]:
                full_name = job.get("name", "")
                job_state = job.get("state", "?").strip()
                print(f"{shot_name:<20} {full_name:<60} state={job_state}")
    else:
        for shot_name in ordered_shots:
            print(shot_name)

    print(f"\n({len(ordered_shots)} unique shot(s))", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
