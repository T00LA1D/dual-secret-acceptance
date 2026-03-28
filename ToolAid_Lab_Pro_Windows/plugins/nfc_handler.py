"""NFC parser plugin."""


def decode_nfc_uid(uid_hex: str) -> dict:
    cleaned = uid_hex.replace(" ", "").lower()
    return {"uid": cleaned, "length": len(cleaned) // 2}
