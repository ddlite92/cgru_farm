#!/usr/bin/env python3
"""Fetch Running/Ready jobs from afserver and emit a regex pattern of their names.

Connects to the Afanasy server, retrieves all jobs whose state matches one of
the requested states (default: Running, Ready), then builds a Python-compatible
regex alternation from the job names.  The pattern is written to stdout so it
can be captured and forwarded to other pipeline scripts (e.g. via --job-mask).

Usage:
    python3 get_active_jobs_regex.py [options]

Options:
    --server SERVER     afserver hostname or IP  (default: 192.168.90.103)
    --port   PORT       afserver TCP port        (default: 51000)
    --states STATES     Comma-separated state names to include
                        (default: Running,Ready)
    --exact             Wrap the pattern in ^(...)$ for full-name matching
    --output FILE       Write the pattern to FILE instead of stdout
    --verbose           Print matched job list to stderr

Examples:
    # Print pattern for all running/ready jobs:
    python3 get_active_jobs_regex.py --verbose

    # Capture and pass to another script:
    PATTERN=$(python3 get_active_jobs_regex.py)
    python3 set_pps_need_properties.py --job-mask "$PATTERN"
"""

import argparse
import re
import sys

import cgruconfig
import af


DEFAULT_SERVER_ADDRESS = "192.168.90.103"
DEFAULT_SERVER_PORT = 51000
# Server returns state as a space-separated flag string, e.g. " RDY OFF" or " RUN DON SKP".
# RDY = ready to run; RUN = has tasks currently executing.
DEFAULT_ACTIVE_STATE_FLAGS = ["RDY", "RUN"]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed argument namespace with server, port, states, exact,
        output, and verbose fields.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Fetch Running/Ready jobs from afserver and emit "
            "a regex pattern of their names."
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
        "--states",
        default=",".join(DEFAULT_ACTIVE_STATE_FLAGS),
        help=(
            "Comma-separated list of state flag tokens to include. "
            "Server uses short flags: RDY (ready), RUN (running), "
            "DON (done), SKP (skipped), SUS (suspended), WDP (waiting deps). "
            f"(default: {','.join(DEFAULT_ACTIVE_STATE_FLAGS)})"
        ),
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Wrap the pattern in ^(...)$ for exact full-name matching.",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        default=None,
        help="Write the regex pattern to FILE instead of stdout.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print matched job details to stderr.",
    )
    return parser.parse_args()


def configure_server(server_address: str, server_port: int) -> None:
    """Override the afserver connection parameters in cgruconfig.

    Must be called before any af.Cmd() instance is created, since
    afnetwork.py reads cgruconfig.VARS at connection time.

    Args:
        server_address: Hostname or IP of the afserver to connect to.
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
            "afserver returned no job data — is afserver running and reachable?"
        )
    return job_list


def filter_jobs_by_state(job_list: list, target_state_flags: list[str]) -> list:
    """Return only jobs whose state string contains at least one target flag.

    The server encodes job state as a space-separated flag string with a
    leading space, e.g. " RDY OFF" or " RUN DON SKP".  A job is included
    if any of its state tokens matches a requested flag (case-insensitive).

    Args:
        job_list: Full list of raw job dicts from the server.
        target_state_flags: State flag tokens to match, e.g. ['RDY', 'RUN'].

    Returns:
        Filtered list of job dicts.
    """
    normalised_targets = {flag.upper() for flag in target_state_flags}
    matching_jobs = []
    for job in job_list:
        job_state_tokens = set(job.get("state", "").split())
        if job_state_tokens & normalised_targets:
            matching_jobs.append(job)
    return matching_jobs


def build_regex_pattern(job_names: list[str], exact_match: bool) -> str:
    """Build a Python-compatible regex alternation from a list of job names.

    Each name is passed through re.escape() to neutralise any regex
    metacharacters present in the job name.

    Args:
        job_names: List of job name strings to include in the pattern.
        exact_match: If True, wraps the alternation in ^(...)$ so the
                     pattern matches the full job name and nothing else.

    Returns:
        A regex pattern string.

    Raises:
        ValueError: If job_names is empty.
    """
    if not job_names:
        raise ValueError("Cannot build a regex pattern from an empty job list.")

    escaped_names = [re.escape(name) for name in job_names]
    alternation = "|".join(escaped_names)

    if exact_match:
        return f"^({alternation})$"
    return alternation


def write_pattern(pattern: str, output_path: str | None) -> None:
    """Write the regex pattern to stdout or a file.

    Args:
        pattern: The regex pattern string to write.
        output_path: File path to write to.  If None, writes to stdout.

    Raises:
        OSError: If the output file cannot be opened for writing.
    """
    if output_path is None:
        print(pattern)
        return

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(pattern + "\n")

    print(f"Pattern written to: {output_path}", file=sys.stderr)


def main() -> int:
    """Connect to afserver, filter active jobs, and emit a regex pattern.

    Returns:
        Exit code: 0 on success, 1 on connection failure or empty result.
    """
    args = parse_args()
    target_states = [state.strip() for state in args.states.split(",") if state.strip()]

    configure_server(args.server, args.port)

    if args.verbose:
        print(
            f"Connecting to afserver at [IP_REDACTED]:{args.port} ...",
            file=sys.stderr,
        )

    cmd = af.Cmd()

    try:
        all_jobs = fetch_all_jobs(cmd, verbose=args.verbose)
    except RuntimeError as fetch_error:
        print(f"ERROR: {fetch_error}", file=sys.stderr)
        return 1

    active_jobs = filter_jobs_by_state(all_jobs, target_states)

    if not active_jobs:
        states_display = ", ".join(target_states)
        print(
            f"No jobs found in state(s): {states_display}",
            file=sys.stderr,
        )
        return 1

    if args.verbose:
        states_display = ", ".join(target_states)
        print(
            f"Found {len(active_jobs)} job(s) in state(s) [{states_display}]:",
            file=sys.stderr,
        )
        for job in active_jobs:
            job_id = job.get("id", "?")
            job_name = job.get("name", "<unnamed>")
            job_state = job.get("state", "?")
            print(f"  [{job_id}] {job_name!r}  state={job_state}", file=sys.stderr)
        print(file=sys.stderr)

    job_names = [job.get("name", "") for job in active_jobs if job.get("name")]

    try:
        regex_pattern = build_regex_pattern(job_names, exact_match=args.exact)
    except ValueError as pattern_error:
        print(f"ERROR: {pattern_error}", file=sys.stderr)
        return 1

    try:
        write_pattern(regex_pattern, args.output)
    except OSError as write_error:
        print(f"ERROR: Could not write output: {write_error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
