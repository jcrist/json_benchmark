import pytest

parser = pytest.importorskip('yyjson')


def parse_document(path, content):
    parser.Document(content).as_obj  # noqa


def test_full_document_read(benchmark, sample_json):
    """
    Benchmarks the performance of completely reading in a document to a Python
    object.
    """
    benchmark.group = f'Complete load of {sample_json[0]}'
    benchmark.name = 'yyjson'
    benchmark.extra_info['file'] = sample_json[0]
    benchmark.extra_info['file_size'] = len(sample_json[1])
    benchmark(parse_document, *sample_json)
