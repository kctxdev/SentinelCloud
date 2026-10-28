"""Coletores por servico."""
from .cloudtrail_collector import collect_cloudtrail
from .iam_collector import collect_iam
from .s3_collector import collect_s3
from .security_groups import collect_security_groups

COLLECTORS = {
    "s3": collect_s3,
    "ec2": collect_security_groups,
    "iam": collect_iam,
    "cloudtrail": collect_cloudtrail,
}

__all__ = ["COLLECTORS"]
