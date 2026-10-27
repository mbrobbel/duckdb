set(SIRIUS_DUCKDB_LINKAGE static CACHE STRING "Sirius library linkage")

duckdb_extension_load(sirius_cuda13
    GIT_URL https://github.com/sirius-db/sirius
    GIT_TAG b4c4ced723ff84eb81cd3b697b1d48d07c8ea98f
    SOURCE_DIR sirius-duckdb
    INCLUDE_DIR sirius-duckdb/src/include
    SUBMODULES "duckdb;cucascade;substrait"
)
