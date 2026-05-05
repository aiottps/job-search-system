import hashlib

def calculate_content_hash(job_item) -> str:
    """
    Calculates a hash for deduplication.
    Uses title, company_name, and location.
    """
    base = f"{job_item.title}|{job_item.company_name}|{job_item.location}"
    return hashlib.sha256(base.encode('utf-8')).hexdigest()

def is_duplicate(job_item, existing_hashes: set) -> bool:
    if job_item.content_hash in existing_hashes:
        return True
    return False
