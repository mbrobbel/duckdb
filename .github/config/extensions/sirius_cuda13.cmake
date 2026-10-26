set(SIRIUS_DUCKDB_LINKAGE static CACHE STRING "Sirius library linkage")

duckdb_extension_load(sirius_cuda13
    GIT_URL https://github.com/sirius-db/sirius
    GIT_TAG 352c3f7e246484b2e76fcd46d7d89de75808ca5e
    SOURCE_DIR sirius-duckdb
    INCLUDE_DIR sirius-duckdb/src/include
    SUBMODULES "duckdb;cucascade;substrait"
)
