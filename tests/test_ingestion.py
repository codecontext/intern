from pathlib import Path

import pytest

from intern.ingestion.service import DocumentIngestionService, IngestionError


def test_ingests_supported_files_recursively_in_path_order(
    tmp_path: Path,
) -> None:
    (tmp_path / "nested").mkdir()
    (tmp_path / "z.md").write_text("markdown", encoding="utf-8")
    (tmp_path / "nested" / "a.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )
    (tmp_path / "ignored.png").write_bytes(b"binary")

    documents = DocumentIngestionService().ingest_directory(tmp_path)

    assert [document.relative_path.as_posix() for document in documents] == [
        "nested/a.py",
        "z.md",
    ]
    assert documents[0].filename == "a.py"
    assert documents[0].extension == ".py"
    assert documents[0].content == "print('hello')"
    assert documents[0].source_path == tmp_path / "nested" / "a.py"
    assert documents[0].size_bytes == len("print('hello')".encode("utf-8"))
    assert documents[0].modified_at.tzinfo is not None


def test_extension_matching_is_case_insensitive(tmp_path: Path) -> None:
    path = tmp_path / "README.MD"
    path.write_text("content", encoding="utf-8")

    documents = DocumentIngestionService().ingest_directory(tmp_path)

    assert len(documents) == 1
    assert documents[0].extension == ".md"


def test_missing_source_directory_raises_ingestion_error(
    tmp_path: Path,
) -> None:
    missing_directory = tmp_path / "missing"

    with pytest.raises(IngestionError, match="does not exist"):
        DocumentIngestionService().ingest_directory(missing_directory)


def test_file_source_path_raises_ingestion_error(tmp_path: Path) -> None:
    source_file = tmp_path / "document.txt"
    source_file.write_text("content", encoding="utf-8")

    with pytest.raises(IngestionError, match="not a directory"):
        DocumentIngestionService().ingest_directory(source_file)


def test_invalid_utf8_raises_ingestion_error(tmp_path: Path) -> None:
    invalid_document = tmp_path / "invalid.txt"
    invalid_document.write_bytes(b"\xff\xfe")

    with pytest.raises(IngestionError, match="valid UTF-8"):
        DocumentIngestionService().ingest_directory(tmp_path)
