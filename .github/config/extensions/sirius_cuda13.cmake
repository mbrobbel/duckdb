set(SIRIUS_DUCKDB_EXTENSION_NAME sirius_cuda13)
set(SIRIUS_DUCKDB_LINKAGE static CACHE STRING "Sirius library linkage")

duckdb_extension_load(sirius_cuda13
    GIT_URL https://github.com/mbrobbel/sirius
    GIT_TAG bdbc13bc2e95810bac40e8fb99d6879d88a46cca
    SOURCE_DIR sirius-duckdb
    INCLUDE_DIR sirius-duckdb/src/include
    SUBMODULES "duckdb;cucascade;substrait"
)
