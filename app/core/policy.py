from enum import StrEnum

from app.core.tenant import TenantContext


class Authority(StrEnum):
    OBSERVE = "AUTH-0"
    RECOMMEND = "AUTH-1"
    DRAFT = "AUTH-2"
    BOUNDED_EXECUTE = "AUTH-3"
    APPROVAL_REQUIRED = "AUTH-4"
    PROHIBITED = "AUTH-5"


class PolicyDecision(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class PolicyDenied(PermissionError):
    pass


AUTHORITY_RANK = {
    Authority.OBSERVE: 0,
    Authority.RECOMMEND: 1,
    Authority.DRAFT: 2,
    Authority.BOUNDED_EXECUTE: 3,
    Authority.APPROVAL_REQUIRED: 4,
    Authority.PROHIBITED: 5,
}


def require_same_tenant(context: TenantContext, resource_tenant_id: str) -> None:
    if context.tenant_id != resource_tenant_id:
        raise PolicyDenied("Cross-tenant access is denied")


def require_authority(
    authority: Authority,
    minimum: Authority,
) -> None:
    if authority is Authority.PROHIBITED or AUTHORITY_RANK[authority] < AUTHORITY_RANK[minimum]:
        raise PolicyDenied("Authority is insufficient for this operation")
