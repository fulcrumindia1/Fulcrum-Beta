"""
QUARANTINED SCRIPT: scripts/remove_requested_accounts.py
=============================================================================
SECURITY NOTICE:
Direct deletion and permanent purge of accounts via unreviewed CLI scripts
is permanently DISABLED by institutional governance and security policy.

Permanent deletion destroys audit history, legal acceptances, relationship
allocations, and Journey events, and risks referential integrity breaches.

All account lifecycle transitions (suspension, archival, scheduled deletion,
and restoration) MUST proceed through the audited Account Lifecycle & Archive
service (services/account_lifecycle.py) and require explicit Sole Platform
Administrator authorization (fulcrumindia1@gmail.com).

Lawful erasure (under applicable data protection regulations like DPDP) must
follow the reviewed, separate lawful erasure protocol with legal hold checks.
=============================================================================
"""

import sys

# Hardcoded operational deletion lists are strictly cleared
EMAILS_TO_REMOVE = []

def main():
    print("FATAL ERROR: Direct account deletion script is QUARANTINED and disabled.")
    print("Direct execution of account purging is prohibited by institutional policy.")
    print("Refer to services/account_lifecycle.py for audited account lifecycle management.")
    sys.exit(1)

if __name__ == "__main__":
    main()
