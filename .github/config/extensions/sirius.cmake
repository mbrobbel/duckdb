duckdb_extension_load(sirius
    DONT_LINK LOAD_TESTS
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG dcdff6e6e898826872df6931545e8cc89192650c
    INCLUDE_DIR src
    TEST_DIR test/sql
    SUBMODULES "duckdb;cucascade;substrait"
)
