set(SIRIUS_DUCKDB_EXTENSION_NAME sirius_cuda13)
set(SIRIUS_DUCKDB_LINKAGE static CACHE STRING "Sirius library linkage")

duckdb_extension_load(sirius_cuda13
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG 4c5bff93faba542f002fdbd587e8cc030b6b8ec7
    SOURCE_DIR sirius-duckdb
    INCLUDE_DIR sirius-duckdb/src/include
    SUBMODULES "duckdb;cucascade;substrait"
)
