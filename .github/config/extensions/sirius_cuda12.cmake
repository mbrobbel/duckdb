set(SIRIUS_DUCKDB_EXTENSION_NAME sirius_cuda12)
set(SIRIUS_DUCKDB_LINKAGE static CACHE STRING "Sirius library linkage")

duckdb_extension_load(sirius_cuda12
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG c408326185457d815acfa8988a6c633e4c4a6da8
    SOURCE_DIR sirius-duckdb
    INCLUDE_DIR sirius-duckdb/src/include
    SUBMODULES "duckdb;cucascade;substrait"
)
