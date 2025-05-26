import pytest
from models.models import ProductSection
from repositories.product_section_repository import ProductSectionRepository
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def section_repo(db):
    return ProductSectionRepository(session=db)

def test_section_create(section_repo):
    section = ProductSection(name="Section Test")
    created = section_repo.create(section)

    assert created.id is not None
    assert created.name == "Section Test"

def test_section_get(section_repo):
    section = ProductSection(name="Section 1")
    section_repo.create(section)

    found = section_repo.get(section.id)
    assert found is not None
    assert found.id == section.id
    assert found.name == "Section 1"

def test_section_get_all(section_repo):

    for s in section_repo.get_all():
        section_repo.delete(s)

    sections = [
        ProductSection(name="Sec1"),
        ProductSection(name="Sec2"),
    ]
    for s in sections:
        section_repo.create(s)

    all_sections = section_repo.get_all()
    assert len(all_sections) >= 2
    names = [s.name for s in all_sections]
    assert "Sec1" in names
    assert "Sec2" in names

def test_section_update(section_repo):
    section = ProductSection(name="Section Test")
    created = section_repo.create(section)

    update_data = {"name": "Section Updated"}
    updated = section_repo.update(created, update_data)

    assert updated.name == "Section Updated"
    assert updated.id == created.id

def test_section_delete(section_repo):
    section = ProductSection(name="Section Delete")
    section_repo.create(section)

    section_id = section.id
    section_repo.delete(section)

    deleted = section_repo.get(section_id)
    assert deleted is None

def test_section_create_duplicate_name(section_repo):
    s1 = ProductSection(name="Duplicated")
    section_repo.create(s1)

    s2 = ProductSection(name="Duplicated")
    with pytest.raises(IntegrityError):
        section_repo.create(s2)
        section_repo.session.rollback()

def test_section_create_missing_name(section_repo):
    section = ProductSection(name=None)
    with pytest.raises(IntegrityError):
        section_repo.create(section)
        section_repo.session.rollback()

def test_section_update_duplicate_name(section_repo):
    s1 = ProductSection(name="Unique1")
    s2 = ProductSection(name="Unique2")
    section_repo.create(s1)
    section_repo.create(s2)

    with pytest.raises(IntegrityError):
        section_repo.update(s2, {"name": "Unique1"})
        section_repo.session.rollback()

def test_section_get_nonexistent(section_repo):
    section = section_repo.get(999999999)
    assert section is None

def test_section_delete_nonexistent(section_repo):
    nonexistent = section_repo.get(999999999)
    assert nonexistent is None
    if nonexistent:
        section_repo.delete(nonexistent)

def test_section_get_all_empty(section_repo):
    for s in section_repo.get_all():
        section_repo.delete(s)

    all_sections = section_repo.get_all()
    assert isinstance(all_sections, list)
    assert len(all_sections) == 0
