set(SIRIUS_DUCKDB_LINKAGE static CACHE STRING "Sirius library linkage")

duckdb_extension_load(sirius_cuda12
    GIT_URL https://github.com/sirius-db/sirius
    GIT_TAG 1493e00ba9021dc383f82b4c584cb13ee07bc306
    SOURCE_DIR sirius-duckdb
    INCLUDE_DIR sirius-duckdb/src/include
    SUBMODULES "duckdb;cucascade;substrait"
)
