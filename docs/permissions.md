# Permissoes necessarias (somente leitura)

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "sts:GetCallerIdentity",
      "s3:ListAllMyBuckets", "s3:GetBucketPublicAccessBlock",
      "s3:GetEncryptionConfiguration", "s3:GetBucketLogging",
      "ec2:DescribeSecurityGroups",
      "iam:ListPolicies", "iam:GetPolicyVersion",
      "cloudtrail:DescribeTrails", "cloudtrail:GetTrailStatus"
    ],
    "Resource": "*"
  }]
}
```

A lista tambem esta em `src/sentinelcloud/aws/permissions.py`.
