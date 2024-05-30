MODULE_PERMISSIONS = {
    "DATA_COLLECTION_FORMS": [
        "iaso_forms",
        "iaso_update_submission",
        "iaso_submissions",
        "iaso_completeness",
        "iaso_completeness_stats",
    ],
    "DEFAULT": [
        "iaso_org_units",
        "iaso_org_unit_types",
        "iaso_org_unit_groups",
        "iaso_sources",
        "iaso_write_sources",
        "iaso_links",
        "iaso_data_tasks",
        "iaso_reports",
        "iaso_projects",
        "iaso_users",
        "iaso_user_roles",
        "iaso_teams",
        "iaso_modules",
    ],
    "DHIS2_MAPPING": ["iaso_mappings"],
    "EMBEDDED_LINKS": ["iaso_pages", "iaso_page_write"],
    "ENTITIES": [
        "iaso_entities",
        "iaso_workflows",
        "iaso_entity_duplicates_write",
        "iaso_entity_duplicates_read",
        "iaso_entity_type_write",
    ],
    "EXTERNAL_STORAGE": ["iaso_storages"],
    "PLANNING": ["iaso_assignments", "iaso_planning_write", "iaso_planning_read"],
    "POLIO_PROJECT": [
        "iaso_polio_config",
        "iaso_polio",
        "iaso_polio_budget_admin",
        "iaso_polio_budget",
        "iaso_polio_vaccine_supply_chain_read",
        "iaso_polio_vaccine_supply_chain_write",
        "iaso_polio_vaccine_stock_management_read",
        "iaso_polio_vaccine_stock_management_write",
        "iaso_polio_notifications",
        "iaso_polio_vaccine_authorizations_read_only",
        "iaso_polio_vaccine_authorizations_admin",
    ],
    "REGISTRY": ["iaso_registry_write", "iaso_registry_read", "iaso_org_unit_change_request_review"],
    "PAYMENTS": ["iaso_payments"],
}

MODULES = [
    {"name": "Data collection - Forms", "codename": "DATA_COLLECTION_FORMS"},
    {"name": "Default", "codename": "DEFAULT"},
    {"name": "DHIS2 mapping", "codename": "DHIS2_MAPPING"},
    {"name": "Embedded links", "codename": "EMBEDDED_LINKS"},
    {"name": "Entities", "codename": "ENTITIES"},
    {"name": "External storage", "codename": "EXTERNAL_STORAGE"},
    {"name": "Planning", "codename": "PLANNING"},
    {"name": "Polio project", "codename": "POLIO_PROJECT"},
    {"name": "Registry", "codename": "REGISTRY"},
    {"name": "Payments", "codename": "PAYMENTS"},
]

FEATUREFLAGES_TO_EXCLUDE = {
    "PLANNING": ["PLANNING"],
    "ENTITIES": [
        "REPORTS",
        "ENTITY",
        "MOBILE_ENTITY_WARN_WHEN_FOUND",
        "MOBILE_ENTITY_LIMITED_SEARCH",
        "MOBILE_ENTITY_NO_CREATION",
        "WRITE_ON_NFC_CARDS",
    ],
}

PERMISSIONS_PRESENTATION = {
    "forms": [
        "iaso_forms",
        "iaso_update_submission",
        "iaso_submissions",
        "iaso_completeness",
        "iaso_completeness_stats",
    ],
    "org_units": [
        "iaso_org_units",
        "iaso_org_unit_types",
        "iaso_org_unit_groups",
        "iaso_sources",
        "iaso_write_sources",
        "iaso_links",
        "iaso_registry_read",
        "iaso_registry_write",
        "iaso_org_unit_change_request_review",
    ],
    "entities": [
        "iaso_entities",
        "iaso_workflows",
        "iaso_entity_duplicates_write",
        "iaso_entity_duplicates_read",
        "iaso_entity_type_write",
    ],
    "payments": ["iaso_payments"],
    "dhis2_mapping": ["iaso_mappings"],
    "external_storage": ["iaso_storages"],
    "planning": ["iaso_assignments", "iaso_planning_write", "iaso_planning_read"],
    "embedded_links": ["iaso_pages", "iaso_page_write"],
    "polio": [
        "iaso_polio_config",
        "iaso_polio",
        "iaso_polio_budget_admin",
        "iaso_polio_budget",
        "iaso_polio_vaccine_supply_chain_read",
        "iaso_polio_vaccine_supply_chain_write",
        "iaso_polio_vaccine_stock_management_read",
        "iaso_polio_vaccine_stock_management_write",
        "iaso_polio_notifications",
        "iaso_polio_vaccine_authorizations_read_only",
        "iaso_polio_vaccine_authorizations_admin",
    ],
    "admin": [
        "iaso_data_tasks",
        "iaso_reports",
        "iaso_projects",
        "iaso_users",
        "iaso_user_roles",
        "iaso_teams",
        "iaso_modules",
    ],
}
