from source_to_skill.templates import slugify


def test_slugify_preserves_cjk_titles():
    assert slugify("金钱心理学：财富、人性和幸福") == "金钱心理学-财富-人性和幸福"
