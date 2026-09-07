"""
ledger.py -- Owned by: Sehaj Mahajan

A simple hash-chain (mock blockchain) audit ledger. Every alert event gets
appended as a tamper-evident block. This simulates the "blockchain-backed
audit trail" -- in production this would be a permissioned chain like
Hyperledger Fabric; here it's an honest, demo-scale stand-in.

Block schema:
    index (int), timestamp (str), event (dict), prev_hash (str), hash (str)
"""

import hashlib
import json
from datetime import datetime


class AuditLedger:
    def __init__(self):
        self.chain = []
        self._add_genesis_block()

    def _hash_block(self, index, timestamp, event, prev_hash):
        block_string = json.dumps(
            {"index": index, "timestamp": timestamp, "event": event, "prev_hash": prev_hash},
            sort_keys=True,
            default=str,
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def _add_genesis_block(self):
        timestamp = datetime.now().isoformat()
        event = {"type": "GENESIS", "detail": "Ledger initialized"}
        block_hash = self._hash_block(0, timestamp, event, "0" * 64)
        self.chain.append({
            "index": 0,
            "timestamp": timestamp,
            "event": event,
            "prev_hash": "0" * 64,
            "hash": block_hash,
        })

    def add_block(self, event: dict):
        prev_hash = self.chain[-1]["hash"]
        index = len(self.chain)
        timestamp = datetime.now().isoformat()
        block_hash = self._hash_block(index, timestamp, event, prev_hash)
        block = {
            "index": index,
            "timestamp": timestamp,
            "event": event,
            "prev_hash": prev_hash,
            "hash": block_hash,
        }
        self.chain.append(block)
        return block

    def get_chain(self):
        return self.chain

    def is_valid(self):
        """Sanity check: verify no block has been tampered with."""
        valid, _ = self.verify_chain()
        return valid

    def verify_chain(self):
        """Verify the full chain and report the FIRST block index where
        tampering is detected (or None if the chain is clean). Used by the
        UI to show exactly where an attacker's edit was caught.
        """
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            recomputed = self._hash_block(
                block["index"], block["timestamp"], block["event"], block["prev_hash"]
            )
            if recomputed != block["hash"]:
                return False, i
            if block["prev_hash"] != self.chain[i - 1]["hash"]:
                return False, i
        return True, None

    def tamper_block(self, index: int, new_event: dict):
        """DEMO-ONLY: simulates an attacker silently editing a past block's
        event data WITHOUT recomputing its hash -- exactly what a real
        attacker would try, and exactly what verify_chain() is designed to
        catch. Never used in the real alert/freeze flow.
        """
        if 0 <= index < len(self.chain):
            self.chain[index]["event"] = new_event


if __name__ == "__main__":
    ledger = AuditLedger()
    ledger.add_block({"type": "ALERT", "ring_id": "RING001", "risk_score": 0.82})
    ledger.add_block({"type": "AUTO_FREEZE", "ring_id": "RING001", "bank": "Mock Bank A"})
    for block in ledger.get_chain():
        print(block["index"], block["event"], block["hash"][:12])
    print("Chain valid:", ledger.is_valid())
