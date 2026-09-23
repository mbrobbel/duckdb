duckdb_extension_load(sirius
    DONT_LINK LOAD_TESTS
    GIT_URL https://github.com/sirius-db/sirius
    GIT_TAG 9912b4456117c1f578f5f91e7514387eeeaf0100
    INCLUDE_DIR src
    TEST_DIR test/sql
    SUBMODULES "duckdb;cucascade;substrait"
)
