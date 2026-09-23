duckdb_extension_load(sirius
    DONT_LINK LOAD_TESTS
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG b8de6bac699938e6f2bfdfdc334fb4729ee33642
    INCLUDE_DIR src
    TEST_DIR test/sql
    SUBMODULES "duckdb;cucascade;substrait"
)
