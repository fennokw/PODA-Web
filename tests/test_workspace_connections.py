def test_repository_map_respects_grant_and_skips_generated_files(client, tmp_folder):
    from poda_app.agent import grants, repository
    (tmp_folder / "main.py").write_text("def start():\n    return 1\n")
    (tmp_folder / "tests").mkdir()
    (tmp_folder / "tests/test_example.py").write_text("def test_example():\n    assert True\n")
    (tmp_folder / "node_modules").mkdir()
    (tmp_folder / "node_modules/internal.py").write_text("def generated():\n    return 2\n")
    outside = tmp_folder.parent / "secret.py"
    outside.write_text("def outside(): pass")
    (tmp_folder / "symlink.py").symlink_to(outside)
    grant = grants.add_grant(str(tmp_folder), "read")
    try:
        result = repository.map_workspace(str(tmp_folder), "test example")["result"]
        assert [e["path"] for e in result["files"]] == ["tests/test_example.py", "main.py"]
        assert result["files"][0]["symbols"][0]["name"] == "test_example"
    finally:
        grants.revoke_grant(grant["id"])


def test_github_publish_uses_atomic_tree_and_checks_readback(monkeypatch):
    from poda_app.agent import tools
    from poda_app.connectors.github import service as github
    repo = "example/project"
    commit, tree, new_tree, head = "a"*40, "b"*40, "c"*40, "d"*40
    calls = []

    def request(target, path="", method="GET", payload=None, **kw):
        assert target == repo
        calls.append((method, path, payload))
        match (method, path.split("?")[0]):
            case ("GET", "/commits/main"): return {"sha": commit, "commit": {"tree": {"sha": tree}}}
            case ("GET", p) if p == "/git/trees/" + tree:
                return {"tree": [{"path": "start.sh", "mode": "100755"}], "truncated": False}
            case ("POST", "/git/trees"):
                assert payload["tree"][0]["mode"] == "100755"
                return {"sha": new_tree}
            case ("POST", "/git/commits"):
                assert payload["parents"] == [commit] and payload["tree"] == new_tree
                return {"sha": head}
            case ("POST", "/git/refs"):
                assert payload == {"ref": "refs/heads/poda/test", "sha": head}
                return {}
            case ("GET", "/pulls"): return []
            case ("POST", "/pulls"):
                assert payload["draft"] is True
                return {"number": 42}
            case ("GET", "/pulls/42"):
                return {"head": {"sha": head}, "base": {"ref": "main"}, "draft": True,
                        "html_url": "https://github.com/example/project/pull/42"}
        raise AssertionError(calls)

    monkeypatch.setattr(github, "_request", request)
    args = tools.validate_args("github_publish_patch", {"repo": repo, "base": "main", "expected_base": commit,
              "branch": "poda/test", "title": "Fix startup", "changes": [{"path": "start.sh", "content": "echo hello\n"}]})
    result = github.publish(**args)
    assert result["result"]["commit"] == head and result["result"]["draft"]


def test_public_reader_rejects_local_or_mixed_addresses(monkeypatch):
    import pytest
    from poda_app.connectors import research

    def mocked(*args, **kwargs):
        return [(None, None, None, None, ("8.8.8.8", 443)), (None, None, None, None, ("127.0.0.1", 443))]
    monkeypatch.setattr(research.socket, "getaddrinfo", mocked)
    with pytest.raises(ValueError, match="public internet"):
        research._address("example.test")
    with pytest.raises(ValueError, match="public HTTPS"):
        research._download("https://user:password@example.test/")
