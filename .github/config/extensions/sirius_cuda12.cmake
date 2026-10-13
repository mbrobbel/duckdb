set(SIRIUS_DUCKDB_EXTENSION_NAME sirius_cuda12)
set(SIRIUS_DUCKDB_LINKAGE static CACHE STRING "Sirius library linkage")

duckdb_extension_load(sirius_cuda12
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG a8655b499d80a32c8625ed2d18c6ad47ea4a81ff
    SOURCE_DIR sirius-duckdb
    INCLUDE_DIR sirius-duckdb/src/include
    SUBMODULES "duckdb;cucascade;substrait"
)
