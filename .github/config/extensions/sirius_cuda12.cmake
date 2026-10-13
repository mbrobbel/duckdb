set(SIRIUS_DUCKDB_EXTENSION_NAME sirius_cuda12)
set(SIRIUS_DUCKDB_LINKAGE static CACHE STRING "Sirius library linkage")

duckdb_extension_load(sirius_cuda12
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG 325031323491f61cc62db251872219b98c96244b
    SOURCE_DIR sirius-duckdb
    INCLUDE_DIR sirius-duckdb/src/include
    SUBMODULES "duckdb;cucascade;substrait"
)
