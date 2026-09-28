duckdb_extension_load(sirius
    DONT_LINK LOAD_TESTS
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG 0db6feb4b3278d44e2f8f5e0a905a0ae18442cee
    INCLUDE_DIR src
    TEST_DIR test/sql
    SUBMODULES "duckdb;cucascade;substrait"
)
