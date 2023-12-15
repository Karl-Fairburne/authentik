# Generated by Django 4.2.7 on 2023-12-15 16:02

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import authentik.core.models
import authentik.stages.authenticator_mobile.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("authentik_flows", "0027_auto_20231028_1424"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuthenticatorMobileStage",
            fields=[
                (
                    "stage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="authentik_flows.stage",
                    ),
                ),
                ("friendly_name", models.TextField(null=True)),
                (
                    "item_matching_mode",
                    models.TextField(
                        choices=[
                            ("accept_deny", "Accept Deny"),
                            ("number_matching_2", "Number Matching 2"),
                            ("number_matching_3", "Number Matching 3"),
                        ],
                        default="number_matching_3",
                    ),
                ),
                ("cgw_endpoint", models.TextField()),
                (
                    "configure_flow",
                    models.ForeignKey(
                        blank=True,
                        help_text="Flow used by an authenticated user to configure this Stage. If empty, user will not be able to configure this stage.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="authentik_flows.flow",
                    ),
                ),
            ],
            options={
                "verbose_name": "Mobile Authenticator Setup Stage",
                "verbose_name_plural": "Mobile Authenticator Setup Stages",
            },
            bases=("authentik_flows.stage", models.Model),
        ),
        migrations.CreateModel(
            name="MobileDevice",
            fields=[
                (
                    "name",
                    models.CharField(
                        help_text="The human-readable name of this device.", max_length=64
                    ),
                ),
                (
                    "confirmed",
                    models.BooleanField(default=True, help_text="Is this device ready for use?"),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("device_id", models.TextField(unique=True)),
                ("firebase_token", models.TextField(blank=True)),
                ("state", models.JSONField(default=dict)),
                ("last_checkin", models.DateTimeField(auto_now=True)),
                (
                    "stage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentik_stages_authenticator_mobile.authenticatormobilestage",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "Mobile Device",
                "verbose_name_plural": "Mobile Devices",
            },
        ),
        migrations.CreateModel(
            name="MobileTransaction",
            fields=[
                (
                    "expires",
                    models.DateTimeField(default=authentik.core.models.default_token_duration),
                ),
                ("expiring", models.BooleanField(default=True)),
                ("tx_id", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("decision_items", models.JSONField(default=list)),
                ("correct_item", models.TextField()),
                ("selected_item", models.TextField(default=None, null=True)),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentik_stages_authenticator_mobile.mobiledevice",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MobileDeviceToken",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "expires",
                    models.DateTimeField(default=authentik.core.models.default_token_duration),
                ),
                ("expiring", models.BooleanField(default=True)),
                (
                    "token",
                    models.TextField(
                        default=authentik.stages.authenticator_mobile.models.default_token_key
                    ),
                ),
                (
                    "device",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentik_stages_authenticator_mobile.mobiledevice",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
