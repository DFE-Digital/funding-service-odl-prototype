from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Address:
    AddressType: str = ""
    Address1: str = ""
    Address2: str = ""
    Address3: str = ""
    Address4: str = ""
    Town: str = ""
    County: str = ""
    Postcode: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "Address":
        if not isinstance(data, dict):
            return cls()
        return cls(
            AddressType=str(data.get("AddressType") or ""),
            Address1=str(data.get("Address1") or ""),
            Address2=str(data.get("Address2") or ""),
            Address3=str(data.get("Address3") or ""),
            Address4=str(data.get("Address4") or ""),
            Town=str(data.get("Town") or ""),
            County=str(data.get("County") or ""),
            Postcode=str(data.get("Postcode") or ""),
        )


@dataclass(slots=True)
class ContactPersonalDetails:
    PersonNameTitle: str = ""
    PersonGivenName: str = ""
    PersonFamilyName: str = ""

    @classmethod
    def from_dict(
        cls, data: dict[str, Any] | None
    ) -> "ContactPersonalDetails":
        if not isinstance(data, dict):
            return cls()
        return cls(
            PersonNameTitle=str(data.get("PersonNameTitle") or ""),
            PersonGivenName=str(data.get("PersonGivenName") or ""),
            PersonFamilyName=str(data.get("PersonFamilyName") or ""),
        )


@dataclass(slots=True)
class PrimaryContact:
    ContactPersonalDetails: ContactPersonalDetails = field(
        default_factory=ContactPersonalDetails
    )
    ContactRole: str = ""
    ContactTelephone1: str = ""
    ContactTelephone2: str = ""
    ContactEmail: str = ""
    Url: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "PrimaryContact":
        if not isinstance(data, dict):
            return cls()
        return cls(
            ContactPersonalDetails=ContactPersonalDetails.from_dict(
                data.get("ContactPersonalDetails")
            ),
            ContactRole=str(data.get("ContactRole") or ""),
            ContactTelephone1=str(data.get("ContactTelephone1") or ""),
            ContactTelephone2=str(data.get("ContactTelephone2") or ""),
            ContactEmail=str(data.get("ContactEmail") or ""),
            Url=str(data.get("Url") or ""),
        )


@dataclass(slots=True)
class VerificationDetail:
    VerificationAuthority: str = ""
    VerificationID: str = ""
    PrimaryVerificationSource: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "VerificationDetail":
        if not isinstance(data, dict):
            return cls()
        return cls(
            VerificationAuthority=str(data.get("VerificationAuthority") or ""),
            VerificationID=str(data.get("VerificationID") or ""),
            PrimaryVerificationSource=bool(data.get("PrimaryVerificationSource") or False),
        )


@dataclass(slots=True)
class ProviderAlias:
    Alias: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ProviderAlias":
        if not isinstance(data, dict):
            return cls()
        return cls(Alias=str(data.get("Alias") or ""))


@dataclass(slots=True)
class ProviderRecord:
    UKPRN: str = ""
    ProviderName: str = ""
    ProviderStatus: str = ""
    VerificationDate: str = ""
    LastUpdated: str = ""
    ICOReference: str | None = None
    LegalAddress: Address = field(default_factory=Address)
    TradingAddresses: list[Address] = field(default_factory=list)
    PrimaryContact: PrimaryContact = field(default_factory=PrimaryContact)
    ProviderAliases: list[ProviderAlias] = field(default_factory=list)
    VerificationDetails: list[VerificationDetail] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ProviderRecord":
        if not isinstance(data, dict):
            return cls()

        trading_addresses = data.get("TradingAddresses")
        if not isinstance(trading_addresses, list):
            trading_addresses = []

        aliases = data.get("ProviderAliases")
        if not isinstance(aliases, list):
            aliases = []

        verification_details = data.get("VerificationDetails")
        if not isinstance(verification_details, list):
            verification_details = []

        ico_reference = data.get("ICOReference")
        if ico_reference is not None:
            ico_reference = str(ico_reference)

        return cls(
            UKPRN=str(data.get("UKPRN") or ""),
            ProviderName=str(data.get("ProviderName") or ""),
            ProviderStatus=str(data.get("ProviderStatus") or ""),
            VerificationDate=str(data.get("VerificationDate") or ""),
            LastUpdated=str(data.get("LastUpdated") or ""),
            ICOReference=ico_reference,
            LegalAddress=Address.from_dict(data.get("LegalAddress")),
            TradingAddresses=[Address.from_dict(item) for item in trading_addresses],
            PrimaryContact=PrimaryContact.from_dict(data.get("PrimaryContact")),
            ProviderAliases=[ProviderAlias.from_dict(item) for item in aliases],
            VerificationDetails=[
                VerificationDetail.from_dict(item) for item in verification_details
            ],
        )


@dataclass(slots=True)
class ProvidersResponse:
    MatchingProviderRecords: list[ProviderRecord] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ProvidersResponse":
        if not isinstance(data, dict):
            return cls()

        records = data.get("MatchingProviderRecords")
        if not isinstance(records, list):
            records = []

        return cls(
            MatchingProviderRecords=[ProviderRecord.from_dict(item) for item in records]
        )
