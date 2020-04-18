# If working with K/V v2
path "secret/data/citrix-adc/*" {
    capabilities = ["read", "list"]
}

# If working with K/V v1
# path "secret/citrix-adc/*" {
#    capabilities = ["read", "list"]
# }
