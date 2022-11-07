# TODO: need better type annotations in this file
from datetime import datetime
from unittest import mock

import pytz
from django.utils import timezone

from iaso.models import Account, Form, MONTH, Instance, OrgUnit, Entity, EntityType, StorageDevice, StorageLogEntry
from iaso.test import APITestCase

MOCK_DATE = datetime(2020, 2, 2, 2, 2, 2, tzinfo=pytz.utc)


class StorageAPITestCase(APITestCase):
    maxDiff = None

    @classmethod
    @mock.patch("django.utils.timezone.now", lambda: MOCK_DATE)
    def setUpTestData(cls):
        cls.star_wars = Account.objects.create(name="Star Wars")
        star_wars_2 = Account.objects.create(name="Star Wars revival")
        cls.yoda = cls.create_user_with_profile(username="yoda", account=cls.star_wars, permissions=["iaso_storages"])

        # Another user that doesn't have the iaso_storages
        cls.another_user = cls.create_user_with_profile(username="yoda2", account=cls.star_wars)

        form_1 = Form.objects.create(name="Hydroponics study", period_type=MONTH, single_per_period=True)

        cls.instance1 = Instance.objects.create(form=form_1, uuid="12345678-1234-1234-1234-123456789012")
        cls.instance2 = Instance.objects.create(form=form_1, uuid="12345678-1234-1234-1234-123456789013")

        cls.org_unit = OrgUnit.objects.create(name="Akkala")
        cls.entity_type = EntityType.objects.create(name="Type 1")
        cls.entity = Entity.objects.create(name="New Client 3", entity_type=cls.entity_type, account=cls.star_wars)

        cls.existing_storage_device = StorageDevice.objects.create(
            customer_chosen_id="EXISTING_STORAGE",
            account=cls.star_wars,
            type="NFC",
            status="OK",
        )

        StorageLogEntry.objects.create(
            id="e4200710-bf82-4d29-a29b-6a042f79ef25",
            device=cls.existing_storage_device,
            operation_type="WRITE_PROFILE",
            performed_by=cls.yoda,
            performed_at=datetime(2022, 10, 13, 13, 12, 56, 0, tzinfo=timezone.utc),
            status="OK",
        )

        cls.existing_storage_device_2 = StorageDevice.objects.create(
            customer_chosen_id="ANOTHER_EXISTING_STORAGE_BLACKLISTED_STOLEN",
            account=cls.star_wars,
            type="NFC",
            status="BLACKLISTED",
            status_reason="STOLEN",
        )

        cls.existing_storage_device_3 = StorageDevice.objects.create(
            customer_chosen_id="ANOTHER_EXISTING_STORAGE_BLACKLISTED_ABUSE",
            account=cls.star_wars,
            type="SD",
            status="BLACKLISTED",
            status_reason="ABUSE",
            entity=cls.entity,
        )

        # This one should be invisible to the "yoda" user
        cls.existing_storage_device_another_account = StorageDevice.objects.create(
            customer_chosen_id="EXISTING_STORAGE_ANOTHER_ACCOUNT",
            account=star_wars_2,
            type="NFC",
        )

    def test_post_log_needs_authentication(self):
        """POST /api/mobile/storage/log/ is rejected if user is not authenticated."""
        response = self.client.post("/api/mobile/storage/logs/")
        self.assertEqual(response.status_code, 403)  # TODO: Would be better to return 401?

    def test_post_log_multiple_logs(self):
        """
        Multiple logs can be sent at once. Based on test_post_storage_base_existing_storage().
        """
        self.client.force_authenticate(self.yoda)

        device = StorageDevice.objects.get(customer_chosen_id="EXISTING_STORAGE", type="NFC", account=self.star_wars)
        num_log_storage_before = StorageLogEntry.objects.filter(device=device).count()

        post_body = [
            {
                "id": "66664567-e89b-12d3-a456-426614174000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "operation_type": "WRITE_RECORD",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": self.org_unit.id,
                "entity_id": self.entity.uuid,
                "performed_at": 1666002739.171,
            },
            {
                "id": "66664567-e89b-12d3-a456-426614175000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "operation_type": "WRITE_RECORD",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": self.org_unit.id,
                "entity_id": self.entity.uuid,
                "performed_at": 1666004000.171,
            },
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")
        self.assertEqual(response.status_code, 201)

        self.assertEqual(StorageLogEntry.objects.count(), num_log_storage_before + 2)

    def test_post_log_base_new_storage(self):
        """
        Test the base of the POST /api/mobile/storage/log/ endpoint, in the case where the storage device is new.

        - Status is 201 CREATED
        - Correct values added to the database
        """

        self.client.force_authenticate(self.yoda)

        num_devices_before = StorageDevice.objects.count()

        post_body = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "storage_id": "NEW_STORAGE",
                "storage_type": "NFC",
                "operation_type": "WRITE_PROFILE",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": self.org_unit.id,
                "entity_id": self.entity.uuid,
                "performed_at": 1666002739.171,  # In seconds
            }
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")

        self.assertEqual(response.status_code, 201)

        # Ensure the storage device was created was decent values
        self.assertEqual(StorageDevice.objects.count(), num_devices_before + 1)
        the_storage = StorageDevice.objects.latest("id")
        self.assertEqual(the_storage.customer_chosen_id, "NEW_STORAGE")
        self.assertEqual(the_storage.account, self.yoda.iaso_profile.account)
        self.assertEqual(the_storage.type, "NFC")
        self.assertEqual(the_storage.status, "OK")

        # Ensure the log entry was created with decent values
        self.assertEqual(the_storage.log_entries.count(), 1)
        the_log_entry = the_storage.log_entries.first()
        self.assertEqual(str(the_log_entry.id), "123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(the_log_entry.operation_type, "WRITE_PROFILE")
        self.assertEqual(str(the_log_entry.performed_at), "2022-10-17 10:32:19+00:00")
        self.assertEqual(the_log_entry.performed_by, self.yoda)
        self.assertQuerysetEqual(the_log_entry.instances.all(), [self.instance1, self.instance2], ordered=False)
        self.assertEqual(the_log_entry.org_unit, self.org_unit)
        self.assertEqual(the_log_entry.entity, self.entity)

        # The "orgunit" and "entity" fields should also have been set on the storage device itself
        self.assertEqual(the_storage.org_unit, self.org_unit)
        self.assertEqual(the_storage.entity, self.entity)

    def test_post_log_base_existing_storage(self):
        """Similar to test_post_storage_base_new_storage, but the storage device already exists."""
        self.client.force_authenticate(self.yoda)

        num_devices_before = StorageDevice.objects.count()

        post_body = [
            {
                "id": "66664567-e89b-12d3-a456-426614174000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "operation_type": "WRITE_RECORD",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": self.org_unit.id,
                "entity_id": self.entity.uuid,
                "performed_at": 1666002739.171,
            }
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")
        self.assertEqual(response.status_code, 201)

        # Ensure the no new devices were created
        self.assertEqual(StorageDevice.objects.count(), num_devices_before)

        the_log_entry = StorageLogEntry.objects.get(id="66664567-e89b-12d3-a456-426614174000")
        self.assertEqual(the_log_entry.device, self.existing_storage_device)

        self.assertEqual(the_log_entry.operation_type, "WRITE_RECORD")
        self.assertEqual(the_log_entry.performed_by, self.yoda)
        self.assertQuerysetEqual(the_log_entry.instances.all(), [self.instance1, self.instance2], ordered=False)
        self.assertEqual(the_log_entry.org_unit, self.org_unit)
        self.assertEqual(the_log_entry.entity, self.entity)
        self.assertEqual(the_log_entry.status, "")
        self.assertEqual(the_log_entry.status_reason, "")

    def test_post_log_existing_update_ou_entity(self):
        """Posting a new log entry to an existing storage device should update its org_unit and entity properties"""
        self.client.force_authenticate(self.yoda)

        new_org_unit = OrgUnit.objects.create(name="Akkala2")
        new_entity = Entity.objects.create(name="New Client 3", entity_type=self.entity_type, account=self.star_wars)

        post_body = [
            {
                "id": "66664567-e89b-12d3-a456-426614174000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "operation_type": "WRITE_RECORD",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": new_org_unit.id,
                "entity_id": new_entity.uuid,
                "performed_at": 1666002739.171,
            }
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")
        self.assertEqual(response.status_code, 201)

        the_log_entry = StorageLogEntry.objects.get(id="66664567-e89b-12d3-a456-426614174000")
        device = the_log_entry.device
        self.assertEqual(device.org_unit, new_org_unit)
        self.assertEqual(device.entity, new_entity)

    def test_post_log_empty_orgunit(self):
        """Posting a new log entry with an empty org_unit_id should be accepted"""
        self.client.force_authenticate(self.yoda)

        post_body = [
            {
                "id": "66664567-e89b-12d3-a456-426614174000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "operation_type": "WRITE_RECORD",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": None,
                "entity_id": self.entity.uuid,
                "performed_at": 1666002739.171,
            }
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")
        self.assertEqual(response.status_code, 201)

        the_log_entry = StorageLogEntry.objects.get(id="66664567-e89b-12d3-a456-426614174000")
        device = the_log_entry.device
        self.assertIsNone(device.org_unit)
        self.assertIsNone(the_log_entry.org_unit)

    def test_post_log_empty_entity(self):
        """Posting a new log entry with an empty entity_id should be accepted"""
        self.client.force_authenticate(self.yoda)

        post_body = [
            {
                "id": "66664567-e89b-12d3-a456-426614174000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "operation_type": "WRITE_RECORD",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": self.org_unit.id,
                "entity_id": None,
                "performed_at": 1666002739.171,
            }
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")
        self.assertEqual(response.status_code, 201)

        the_log_entry = StorageLogEntry.objects.get(id="66664567-e89b-12d3-a456-426614174000")
        device = the_log_entry.device
        self.assertIsNone(device.entity)
        self.assertIsNone(the_log_entry.entity)

    def test_post_log_invalid_storage_type(self):
        """In the case the storage type is invalid, POST to /api/mobile/storage/log/ should return 400."""
        self.client.force_authenticate(self.yoda)

        num_logs_before = StorageLogEntry.objects.count()
        post_body = [
            {
                "id": "66664567-e89b-12d3-a456-426614174000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "INVALID_TYPE",
                "operation_type": "WRITE_RECORD",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": self.org_unit.id,
                "entity_id": self.entity.uuid,
                "performed_at": 1666002739.171,
            }
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")
        self.assertEqual(response.status_code, 400)
        # Also make sure nothing was added to the database
        self.assertEqual(StorageLogEntry.objects.count(), num_logs_before)

    def test_post_log_invalid_operation_type(self):
        """In the case the operation type is invalid, POST to /api/mobile/storage/log/ should return 400."""
        self.client.force_authenticate(self.yoda)

        num_logs_before = StorageLogEntry.objects.count()
        post_body = [
            {
                "id": "66664567-e89b-12d3-a456-426614174000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "operation_type": "INVALID_OPERATION_TYPE",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": self.org_unit.id,
                "entity_id": self.entity.uuid,
                "performed_at": 1666002739.171,
            }
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")
        self.assertEqual(response.status_code, 400)
        # Also make sure nothing was added to the database
        self.assertEqual(StorageLogEntry.objects.count(), num_logs_before)

    def test_post_log_invalid_org_unit(self):
        """In the case the org unit is invalid, POST to /api/mobile/storage/log/ should return 400."""
        self.client.force_authenticate(self.yoda)

        num_logs_before = StorageLogEntry.objects.count()
        post_body = [
            {
                "id": "66664567-e89b-12d3-a456-426614174000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "operation_type": "WRITE_RECORD",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": 9999,
                "entity_id": self.entity.uuid,
                "performed_at": 1666002739.171,
            }
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")
        self.assertEqual(response.status_code, 400)
        # Also make sure nothing was added to the database
        self.assertEqual(StorageLogEntry.objects.count(), num_logs_before)

    def test_post_log_invalid_entity(self):
        """In the case the entity is invalid, POST to /api/mobile/storage/log/ should return 400."""
        self.client.force_authenticate(self.yoda)

        num_logs_before = StorageLogEntry.objects.count()
        post_body = [
            {
                "id": "66664567-e89b-12d3-a456-426614174000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "operation_type": "WRITE_RECORD",
                "instances": [self.instance1.uuid, self.instance2.uuid],
                "org_unit_id": self.org_unit.id,
                "entity_id": 9999,
                "performed_at": 1666002739.171,
            }
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")
        self.assertEqual(response.status_code, 400)
        # Also make sure nothing was added to the database
        self.assertEqual(StorageLogEntry.objects.count(), num_logs_before)

    def test_post_log_empty_instances(self):
        """Posting a new log entry with an empty instances list should be accepted"""
        self.client.force_authenticate(self.yoda)

        post_body = [
            {
                "id": "66664567-e89b-12d3-a456-426614174000",
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "operation_type": "WRITE_RECORD",
                "instances": [],
                "org_unit_id": self.org_unit.id,
                "entity_id": self.entity.uuid,
                "performed_at": 1666002739.171,
            }
        ]
        response = self.client.post("/api/mobile/storage/logs/", post_body, format="json")
        self.assertEqual(response.status_code, 201)

        the_log_entry = StorageLogEntry.objects.get(id="66664567-e89b-12d3-a456-426614174000")
        self.assertEqual(the_log_entry.instances.count(), 0)

    def test_post_existing_logs(self):
        """If a storage log entry already exists, it should be silently ignored if pushed again"""
        pass

    # TODO: POST test mandatory fields are checked on POST
    # TODO: POST test an error is returned if incorrect value for instances, org unit or entity (400)

    def test_list_only_authenticated(self):
        """GET /api/storage/ is rejected if user is not authenticated."""
        response = self.client.get("/api/storage/")
        self.assertEqual(response.status_code, 403)
        # TODO: according to the specs, it should be 401.
        #  Is that consistent with the rest of the API? (fix/or update specs)

    def test_list_only_storages_permission(self):
        """GET /api/storage/ is rejected if user does not have the 'storages' permission."""
        self.client.force_authenticate(self.another_user)
        response = self.client.get("/api/storage/")
        self.assertEqual(response.status_code, 403)

    def test_list_base(self):
        """
        GET /api/storage/ return a status 200 and the list of devices in the specified format.

        We also check that devices from other accounts (than the user account) are not returned.

        Endpoint specs: https://bluesquare.atlassian.net/browse/WC2-62
        """
        self.client.force_authenticate(self.yoda)
        response = self.client.get("/api/storage/")
        self.assertEqual(response.status_code, 200)
        received_json = response.json()
        self.assertEqual(
            received_json,
            [
                {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "EXISTING_STORAGE",
                    "storage_type": "NFC",
                    "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": None,
                },
                {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "ANOTHER_EXISTING_STORAGE_BLACKLISTED_STOLEN",
                    "storage_type": "NFC",
                    "status": {"status": "BLACKLISTED", "reason": "STOLEN", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": None,
                },
                {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "ANOTHER_EXISTING_STORAGE_BLACKLISTED_ABUSE",
                    "storage_type": "SD",
                    "status": {"status": "BLACKLISTED", "reason": "ABUSE", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": {"id": self.entity.id, "name": "New Client 3"},
                },
            ],
        )

    def test_list_filter_by_status(self):
        """GET /api/storage/?status=OK only returns devices with the specified status"""
        self.client.force_authenticate(self.yoda)
        response = self.client.get("/api/storage/?status=BLACKLISTED")
        received_json = response.json()
        self.assertEqual(
            received_json,
            [
                {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "ANOTHER_EXISTING_STORAGE_BLACKLISTED_STOLEN",
                    "storage_type": "NFC",
                    "status": {"status": "BLACKLISTED", "reason": "STOLEN", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": None,
                },
                {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "ANOTHER_EXISTING_STORAGE_BLACKLISTED_ABUSE",
                    "storage_type": "SD",
                    "status": {"status": "BLACKLISTED", "reason": "ABUSE", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": {"id": self.entity.id, "name": "New Client 3"},
                },
            ],
        )

    # TODO: list: error 400 if incorrect status/reason/type is requested?

    def test_list_filter_by_reason(self):
        """GET /api/storage/?status=OK only returns devices with the specified status"""
        self.client.force_authenticate(self.yoda)
        response = self.client.get("/api/storage/?reason=STOLEN")
        received_json = response.json()
        self.assertEqual(
            received_json,
            [
                {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "ANOTHER_EXISTING_STORAGE_BLACKLISTED_STOLEN",
                    "storage_type": "NFC",
                    "status": {"status": "BLACKLISTED", "reason": "STOLEN", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": None,
                }
            ],
        )

    def test_list_filter_by_type(self):
        """GET /api/storage/?status=OK only returns devices with the specified type"""
        self.client.force_authenticate(self.yoda)
        response = self.client.get("/api/storage/?type=NFC")
        received_json = response.json()
        self.assertEqual(
            received_json,
            [
                {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "EXISTING_STORAGE",
                    "storage_type": "NFC",
                    "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": None,
                },
                {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "ANOTHER_EXISTING_STORAGE_BLACKLISTED_STOLEN",
                    "storage_type": "NFC",
                    "status": {"status": "BLACKLISTED", "reason": "STOLEN", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": None,
                },
            ],
        )

    def test_list_filter_by_storage_id(self):
        """The 'search' filter can be used to filter per (customer-chosen) storage ID"""
        self.client.force_authenticate(self.yoda)
        response = self.client.get("/api/storage/?search=aNotHeR")
        received_json = response.json()

        # If the filter was not operational we would get 3 results.
        # If the filter was not case-insensitive we would get 0 results.
        self.assertEqual(len(received_json), 2)
        # We double-check that the results are the ones we expect
        for entry in received_json:
            self.assertIn("ANOTHER", entry["storage_id"])

    def test_list_filter_by_entity_id(self):
        """The 'search' filter can be also be used to search per entity ID"""
        self.client.force_authenticate(self.yoda)
        response = self.client.get(f"/api/storage/?search={self.entity.id}")
        received_json = response.json()

        # If the filter was not operational we would get 3 results.
        self.assertEqual(
            received_json,
            [
                {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "ANOTHER_EXISTING_STORAGE_BLACKLISTED_ABUSE",
                    "storage_type": "SD",
                    "status": {"status": "BLACKLISTED", "reason": "ABUSE", "updated_at": None, "comment": ""},
                    "org_unit": None,
                    "entity": {"id": self.entity.id, "name": "New Client 3"},
                }
            ],
        )

    def test_list_can_be_ordered(self):
        """GET /api/storage/ takes an optional parameter to order the results (default: updated_at)"""
        self.client.force_authenticate(self.yoda)
        response = self.client.get("/api/storage/?order=-type")
        received_json = response.json()
        types_in_order_received = [entry["storage_type"] for entry in received_json]
        self.assertEqual(types_in_order_received[::-1], sorted(types_in_order_received))
        # TODO: check with the frontend team which exact ordering possibilities should be available

    def test_list_can_be_paginated(self):
        """GET /api/storage/ takes an optional "limit" parameter to paginate the results"""
        self.client.force_authenticate(self.yoda)
        response = self.client.get("/api/storage/?limit=1")
        received_json = response.json()
        self.assertEqual(received_json["count"], 3)  # 3 devices in total
        self.assertEqual(len(received_json["results"]), 1)  # 1 result on this page
        self.assertEqual(received_json["pages"], 3)  # 3 pages of results
        self.assertTrue(received_json["has_next"])
        self.assertFalse(received_json["has_previous"])
        self.assertEqual(received_json["limit"], 1)

    def test_post_blacklisted_storage_permission_denied(self):
        """POST to /api/storage/blacklisted requires an authenticated user with iaso_storage permissions"""
        # Case 1: anonymous user
        response = self.client.post(
            "/api/storage/blacklisted/",
            {
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "storage_status": {"status": "BLACKLISTED", "reason": "DAMAGED", "comment": "not usable anymore"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

        # Case 2: user without iaso_storage permissions
        self.client.force_authenticate(self.another_user)

        response = self.client.post(
            "/api/storage/blacklisted/",
            {
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "storage_status": {"status": "BLACKLISTED", "reason": "DAMAGED", "comment": "not usable anymore"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_post_blacklisted_storage_ok(self):
        """
        POST /api/storage/blacklisted with correct parameters and permissions does the job:

        - returns the 200 status
        - perform the requested changes in the database
        """
        self.client.force_authenticate(self.yoda)

        post_body = {
            "storage_id": "EXISTING_STORAGE",
            "storage_type": "NFC",
            "storage_status": {"status": "BLACKLISTED", "reason": "DAMAGED", "comment": "not usable anymore"},
        }

        with mock.patch("django.utils.timezone.now", wraps=lambda: datetime(2022, 10, 26, 2, 2, 2, tzinfo=pytz.utc)):
            response = self.client.post("/api/storage/blacklisted/", post_body, format="json")

        self.assertEqual(response.status_code, 200)

        # check that the storage status has been updated (was OK before)
        updated_storage = StorageDevice.objects.get(pk=self.existing_storage_device.pk)
        self.assertEqual(updated_storage.status, "BLACKLISTED")
        self.assertEqual(updated_storage.status_reason, "DAMAGED")
        self.assertEqual(updated_storage.status_comment, "not usable anymore")
        self.assertEqual(str(updated_storage.status_updated_at), "2022-10-26 02:02:02+00:00")

        # check that a corresponding log entry has been created

        latest_log_entry_for_storage = updated_storage.log_entries.latest("performed_at")
        self.assertEqual(latest_log_entry_for_storage.operation_type, "CHANGE_STATUS")
        self.assertEqual(latest_log_entry_for_storage.performed_by, self.yoda)
        self.assertEqual(latest_log_entry_for_storage.status, "BLACKLISTED")
        self.assertEqual(latest_log_entry_for_storage.status_reason, "DAMAGED")
        self.assertEqual(latest_log_entry_for_storage.status_comment, "not usable anymore")
        # TODO: also check the value of performed_at (use mock object?)

    def test_post_blacklisted_storage_non_existing(self):
        """An error 400 is returned if we try to blacklist a non-existing device"""
        self.client.force_authenticate(self.yoda)

        post_body = {
            "storage_id": "NON_EXISTING_STORAGE",
            "storage_type": "NFC",
            "storage_status": {"status": "BLACKLISTED", "reason": "DAMAGED", "comment": "not usable anymore"},
        }
        response = self.client.post("/api/storage/blacklisted/", post_body, format="json")
        self.assertEqual(response.status_code, 400)

    def test_post_blacklisted_storage_incorrect_status(self):
        """An error 400 is returned if we try to blacklist a device with an incorrect status"""
        self.client.force_authenticate(self.yoda)

        post_body = {
            "storage_id": "EXISTING_STORAGE",
            "storage_type": "NFC",
            "storage_status": {"status": "AZFDSGFDDFFD", "reason": "DAMAGED", "comment": "not usable anymore"},
        }
        response = self.client.post("/api/storage/blacklisted/", post_body, format="json")
        self.assertEqual(response.status_code, 400)

    def test_post_blacklisted_storage_incorrect_reason(self):
        """An error 400 is returned if we try to blacklist a device for an incorrect reason"""
        self.client.force_authenticate(self.yoda)

        post_body = {
            "storage_id": "EXISTING_STORAGE",
            "storage_type": "NFC",
            "storage_status": {"status": "BLACKLISTED", "reason": "AZFDSGFDDFFD", "comment": "not usable anymore"},
        }
        response = self.client.post("/api/storage/blacklisted/", post_body, format="json")
        self.assertEqual(response.status_code, 400)

    def test_post_blacklisted_reason_mandatory_when_blacklisting(self):
        """An error 400 is returned if we try to blacklist a device without specifying a reason"""
        self.client.force_authenticate(self.yoda)

        post_body = {
            "storage_id": "EXISTING_STORAGE",
            "storage_type": "NFC",
            "storage_status": {"status": "BLACKLISTED", "reason": None, "comment": "not usable anymore"},
        }
        response = self.client.post("/api/storage/blacklisted/", post_body, format="json")
        self.assertEqual(response.status_code, 400)

    def test_get_logs_for_device_unauthenticated(self):
        """A non authenticated user should receive a 403"""
        response = self.client.get("/api/storage/NFC/EXISTING_STORAGE/logs")
        self.assertEqual(response.status_code, 403)

    def test_get_logs_for_device_insufficient_permissions(self):
        """A user without the "iaso_storages" permission should receive a 403"""
        self.client.force_authenticate(self.another_user)
        response = self.client.get("/api/storage/NFC/EXISTING_STORAGE/logs")
        self.assertEqual(response.status_code, 403)

    def test_get_logs_for_device_base(self):
        """Test the basics of the logs per device endpoint"""
        self.client.force_authenticate(self.yoda)
        response = self.client.get("/api/storage/NFC/EXISTING_STORAGE/logs")
        self.assertEqual(response.status_code, 200)
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "updated_at": 1580608922.0,
                "created_at": 1580608922.0,
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                "org_unit": None,
                "entity": None,
                "logs": [
                    {
                        "id": "e4200710-bf82-4d29-a29b-6a042f79ef25",
                        "storage_id": "EXISTING_STORAGE",
                        "storage_type": "NFC",
                        "operation_type": "WRITE_PROFILE",
                        "instances": [],
                        "org_unit": None,
                        "entity": None,
                        "performed_at": 1665666776.0,
                        "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                        "status": "OK",
                        "status_comment": "",
                        "status_reason": "",
                    }
                ],
            },
        )

    def test_get_logs_for_device_ou_filter(self):
        """The logs per device endpoint can be filtered by org_unit_id"""
        self.client.force_authenticate(self.yoda)
        # 1. Case one: no logs because no log entries for this device refer to the given OU
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?org_unit_id={self.org_unit.id}")

        self.assertEqual(response.status_code, 200)
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "updated_at": 1580608922.0,
                "created_at": 1580608922.0,
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                "org_unit": None,
                "entity": None,
                "logs": [],
            },
        )

        # Case 2: we add one log entry for the given device and OU
        StorageLogEntry.objects.create(
            id="e4200710-bf82-4d29-a29b-6a042f79ef26",
            device=self.existing_storage_device,
            operation_type="WRITE_PROFILE",
            performed_by=self.yoda,
            performed_at=datetime(2022, 10, 13, 13, 12, 56, 0, tzinfo=timezone.utc),
            org_unit=self.org_unit,
            status="BLACKLISTED",
            status_reason="DAMAGED",
            status_comment="not usable anymore",
        )

        # This time, it should be returned
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?org_unit_id={self.org_unit.id}")
        received_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            received_json,
            {
                "updated_at": 1580608922.0,
                "created_at": 1580608922.0,
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                "org_unit": None,
                "entity": None,
                "logs": [
                    {
                        "id": "e4200710-bf82-4d29-a29b-6a042f79ef26",
                        "storage_id": "EXISTING_STORAGE",
                        "storage_type": "NFC",
                        "operation_type": "WRITE_PROFILE",
                        "instances": [],
                        "org_unit": {"id": self.org_unit.id, "name": "Akkala"},
                        "entity": None,
                        "performed_at": 1665666776.0,
                        "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                        "status": "BLACKLISTED",
                        "status_comment": "not usable anymore",
                        "status_reason": "DAMAGED",
                    }
                ],
            },
        )

    def test_get_logs_for_device_types_filter(self):
        """The logs per device endpoint can be filtered by org_unit_id"""
        self.client.force_authenticate(self.yoda)

        # Case 1: we request WRITE_PROFILE, there is one from setupTestData
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?types=WRITE_PROFILE")
        received_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            received_json,
            {
                "updated_at": 1580608922.0,
                "created_at": 1580608922.0,
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                "org_unit": None,
                "entity": None,
                "logs": [
                    {
                        "id": "e4200710-bf82-4d29-a29b-6a042f79ef25",
                        "storage_id": "EXISTING_STORAGE",
                        "storage_type": "NFC",
                        "operation_type": "WRITE_PROFILE",
                        "instances": [],
                        "org_unit": None,
                        "entity": None,
                        "performed_at": 1665666776.0,
                        "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                        "status": "OK",
                        "status_comment": "",
                        "status_reason": "",
                    }
                ],
            },
        )

        # Case 2: we request WRITE_RECORD, there's currently none
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?types=WRITE_RECORD")
        self.assertEqual(response.status_code, 200)
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "updated_at": 1580608922.0,
                "created_at": 1580608922.0,
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                "org_unit": None,
                "entity": None,
                "logs": [],
            },
        )

        # Case 3: we request both, there's currently only one WRITE_PROFILE
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?types=WRITE_PROFILE,WRITE_RECORD")
        self.assertEqual(response.status_code, 200)
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "updated_at": 1580608922.0,
                "created_at": 1580608922.0,
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                "org_unit": None,
                "entity": None,
                "logs": [
                    {
                        "id": "e4200710-bf82-4d29-a29b-6a042f79ef25",
                        "storage_id": "EXISTING_STORAGE",
                        "storage_type": "NFC",
                        "operation_type": "WRITE_PROFILE",
                        "instances": [],
                        "org_unit": None,
                        "entity": None,
                        "performed_at": 1665666776.0,
                        "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                        "status": "OK",
                        "status_comment": "",
                        "status_reason": "",
                    }
                ],
            },
        )

        # Case 4: we add an entry for WRITE_RECORD, we can now request both again and see them
        StorageLogEntry.objects.create(
            id="e4200710-bf82-4d29-a29b-6a042f79ef26",
            device=self.existing_storage_device,
            operation_type="WRITE_RECORD",
            performed_by=self.yoda,
            performed_at=datetime(2022, 10, 13, 13, 12, 56, 0, tzinfo=timezone.utc),
            org_unit=self.org_unit,
        )

        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?types=WRITE_PROFILE,WRITE_RECORD&order=id")
        self.assertEqual(response.status_code, 200)
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "updated_at": 1580608922.0,
                "created_at": 1580608922.0,
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                "org_unit": None,
                "entity": None,
                "logs": [
                    {
                        "id": "e4200710-bf82-4d29-a29b-6a042f79ef25",
                        "storage_id": "EXISTING_STORAGE",
                        "storage_type": "NFC",
                        "operation_type": "WRITE_PROFILE",
                        "instances": [],
                        "org_unit": None,
                        "entity": None,
                        "performed_at": 1665666776.0,
                        "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                        "status": "OK",
                        "status_comment": "",
                        "status_reason": "",
                    },
                    {
                        "id": "e4200710-bf82-4d29-a29b-6a042f79ef26",
                        "storage_id": "EXISTING_STORAGE",
                        "storage_type": "NFC",
                        "operation_type": "WRITE_RECORD",
                        "instances": [],
                        "org_unit": {"id": self.org_unit.id, "name": "Akkala"},
                        "entity": None,
                        "performed_at": 1665666776.0,
                        "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                        "status": "",
                        "status_comment": "",
                        "status_reason": "",
                    },
                ],
            },
        )

    def test_get_logs_for_device_status_filter(self):
        """The logs per device endpoint can be filtered by status"""
        self.client.force_authenticate(self.yoda)

        # Case 1: we request the OK status, there is one from setupTestData
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?status=OK")
        self.assertEqual(response.status_code, 200)
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "updated_at": 1580608922.0,
                "created_at": 1580608922.0,
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                "org_unit": None,
                "entity": None,
                "logs": [
                    {
                        "id": "e4200710-bf82-4d29-a29b-6a042f79ef25",
                        "storage_id": "EXISTING_STORAGE",
                        "storage_type": "NFC",
                        "operation_type": "WRITE_PROFILE",
                        "instances": [],
                        "org_unit": None,
                        "entity": None,
                        "performed_at": 1665666776.0,
                        "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                        "status": "OK",
                        "status_comment": "",
                        "status_reason": "",
                    }
                ],
            },
        )

        # Case 2: we request the blacklisted status, there is none
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?status=BLACKLISTED")
        self.assertEqual(response.status_code, 200)
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "updated_at": 1580608922.0,
                "created_at": 1580608922.0,
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                "org_unit": None,
                "entity": None,
                "logs": [],
            },
        )

    def test_get_logs_for_device_reason_filter(self):
        """The logs per device endpoint can be filtered by (status) reason"""
        self.client.force_authenticate(self.yoda)

        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?reason=STOLEN")
        self.assertEqual(response.status_code, 200)
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "updated_at": 1580608922.0,
                "created_at": 1580608922.0,
                "storage_id": "EXISTING_STORAGE",
                "storage_type": "NFC",
                "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                "org_unit": None,
                "entity": None,
                "logs": [],
            },
        )

    def test_get_logs_for_device_pagination(self):
        """The logs per device endpoint can optionally be paginated"""
        self.client.force_authenticate(self.yoda)

        # We first add a second log for this device, so we have more realistic test data
        StorageLogEntry.objects.create(
            id="e4200710-bf82-4d29-a29b-6a042f79ef26",
            device=self.existing_storage_device,
            operation_type="WRITE_PROFILE",
            performed_by=self.yoda,
            performed_at=datetime(2022, 10, 13, 13, 12, 56, 0, tzinfo=timezone.utc),
        )

        # We request the first page
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?limit=1&page=1&order=id")
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "count": 2,
                "results": {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "EXISTING_STORAGE",
                    "storage_type": "NFC",
                    "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": None,
                    "logs": [
                        {
                            "id": "e4200710-bf82-4d29-a29b-6a042f79ef25",
                            "storage_id": "EXISTING_STORAGE",
                            "storage_type": "NFC",
                            "operation_type": "WRITE_PROFILE",
                            "instances": [],
                            "org_unit": None,
                            "entity": None,
                            "performed_at": 1665666776.0,
                            "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                            "status": "OK",
                            "status_comment": "",
                            "status_reason": "",
                        }
                    ],
                },
                "has_next": True,
                "has_previous": False,
                "page": 1,
                "pages": 2,
                "limit": 1,
            },
        )

        # Then the second
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?limit=1&page=2&order=id")
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "count": 2,
                "results": {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "EXISTING_STORAGE",
                    "storage_type": "NFC",
                    "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": None,
                    "logs": [
                        {
                            "id": "e4200710-bf82-4d29-a29b-6a042f79ef26",
                            "storage_id": "EXISTING_STORAGE",
                            "storage_type": "NFC",
                            "operation_type": "WRITE_PROFILE",
                            "instances": [],
                            "org_unit": None,
                            "entity": None,
                            "performed_at": 1665666776.0,
                            "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                            "status": "",
                            "status_comment": "",
                            "status_reason": "",
                        }
                    ],
                },
                "has_next": False,
                "has_previous": True,
                "page": 2,
                "pages": 2,
                "limit": 1,
            },
        )

        # Then both records on the same page
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?limit=10&page=1&order=id")
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "count": 2,
                "results": {
                    "updated_at": 1580608922.0,
                    "created_at": 1580608922.0,
                    "storage_id": "EXISTING_STORAGE",
                    "storage_type": "NFC",
                    "status": {"status": "OK", "reason": "", "comment": "", "updated_at": None},
                    "org_unit": None,
                    "entity": None,
                    "logs": [
                        {
                            "id": "e4200710-bf82-4d29-a29b-6a042f79ef25",
                            "storage_id": "EXISTING_STORAGE",
                            "storage_type": "NFC",
                            "operation_type": "WRITE_PROFILE",
                            "instances": [],
                            "org_unit": None,
                            "entity": None,
                            "performed_at": 1665666776.0,
                            "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                            "status": "OK",
                            "status_comment": "",
                            "status_reason": "",
                        },
                        {
                            "id": "e4200710-bf82-4d29-a29b-6a042f79ef26",
                            "storage_id": "EXISTING_STORAGE",
                            "storage_type": "NFC",
                            "operation_type": "WRITE_PROFILE",
                            "instances": [],
                            "org_unit": None,
                            "entity": None,
                            "performed_at": 1665666776.0,
                            "performed_by": {"first_name": "", "last_name": "", "username": "yoda"},
                            "status": "",
                            "status_comment": "",
                            "status_reason": "",
                        },
                    ],
                },
                "has_next": False,
                "has_previous": False,
                "page": 1,
                "pages": 1,
                "limit": 10,
            },
        )

    def test_get_logs_for_device_pagination_correct_count(self):
        """Regression test: the 'count' attributes of the paginator listed the log entries for all devices."""
        self.client.force_authenticate(self.yoda)

        # We first add a second log for another device, it shouldn't appear in the count of other devices
        StorageLogEntry.objects.create(
            id="e4200710-bf82-4d29-a29b-6a042f79ef26",
            device=self.existing_storage_device_2,
            operation_type="WRITE_PROFILE",
            performed_by=self.yoda,
            performed_at=datetime(2022, 10, 13, 13, 12, 56, 0, tzinfo=timezone.utc),
        )

        # We request the first page
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?limit=1&page=1&order=id")
        received_json = response.json()
        self.assertEqual(received_json["count"], 1)

    def test_get_logs_per_device_order(self):
        """Test various ordering options for the logs per device endpoint"""
        self.client.force_authenticate(self.yoda)

        # We add another one for more realistic test data
        StorageLogEntry.objects.create(
            id="e4200710-bf82-4d29-a29b-6a042f79ef26",
            device=self.existing_storage_device,
            operation_type="WRITE_RECORD",
            performed_by=self.yoda,
            performed_at=datetime(2022, 10, 15, 13, 12, 56, 0, tzinfo=timezone.utc),
            org_unit=self.org_unit,
        )

        # Ordering by "id"
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?order=id")
        received_json = response.json()
        received_data = [e["id"] for e in received_json["logs"]]
        self.assertEqual(received_data, sorted(received_data))

        # Ordering by reverse "id"
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?order=-id")
        received_json = response.json()
        received_data = [e["id"] for e in received_json["logs"]]
        self.assertEqual(received_data[::-1], sorted(received_data))

        # Ordering by "operation_type"
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?order=operation_type")
        received_json = response.json()
        received_data = [e["operation_type"] for e in received_json["logs"]]
        self.assertEqual(received_data, sorted(received_data))

        # Ordering by reverse "operation_type"
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?order=-operation_type")
        received_json = response.json()
        received_data = [e["operation_type"] for e in received_json["logs"]]
        self.assertEqual(received_data[::-1], sorted(received_data))

        # Ordering by "performed_at"
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?order=performed_at")
        received_json = response.json()
        received_data = [e["performed_at"] for e in received_json["logs"]]
        self.assertEqual(received_data, sorted(received_data))

        # Ordering by reverse "performed_at"
        response = self.client.get(f"/api/storage/NFC/EXISTING_STORAGE/logs?order=-performed_at")
        received_json = response.json()
        received_data = [e["performed_at"] for e in received_json["logs"]]
        self.assertEqual(received_data[::-1], sorted(received_data))

    def test_get_blacklisted_devices(self):
        """Test the basics of the GET /api/mobile/storage/blacklisted endpoint"""
        response = self.client.get("/api/mobile/storage/blacklisted/")
        self.assertEqual(response.status_code, 200)
        received_json = response.json()
        self.assertEqual(
            received_json,
            {
                "storages": [
                    {
                        "updated_at": 1580608922.0,
                        "created_at": 1580608922.0,
                        "storage_id": "ANOTHER_EXISTING_STORAGE_BLACKLISTED_STOLEN",
                        "storage_type": "NFC",
                        "status": {"status": "BLACKLISTED", "reason": "STOLEN", "comment": "", "updated_at": None},
                        "org_unit": None,
                        "entity": None,
                    },
                    {
                        "updated_at": 1580608922.0,
                        "created_at": 1580608922.0,
                        "storage_id": "ANOTHER_EXISTING_STORAGE_BLACKLISTED_ABUSE",
                        "storage_type": "SD",
                        "status": {"status": "BLACKLISTED", "reason": "ABUSE", "comment": "", "updated_at": None},
                        "org_unit": None,
                        "entity": {"id": self.entity.id, "name": "New Client 3"},
                    },
                ]
            },
        )