set(SIRIUS_DUCKDB_EXTENSION_NAME sirius_cuda12)
set(SIRIUS_DUCKDB_LINKAGE static CACHE STRING "Sirius library linkage")

duckdb_extension_load(sirius_cuda12
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG 8996dec1606fe87dbc7eb845bcbaac483aa4d3c6
    SOURCE_DIR sirius-duckdb
    INCLUDE_DIR sirius-duckdb/src/include
    SUBMODULES "duckdb;cucascade;substrait"
)
