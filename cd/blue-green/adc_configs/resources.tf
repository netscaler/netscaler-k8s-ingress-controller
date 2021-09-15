resource "citrixadc_csvserver" "demo_csvserver" {
  ipv46       = "<Enter the ADC Frontend IP>"
  name        = "demo_csvserver"
  port        = 80
  servicetype = "HTTP"
}

resource "citrixadc_lbvserver"  "lbvs"{
  name        = format("%s-lbvs", var.resource_prefix)
  servicetype = "HTTP"
}

resource "citrixadc_service"  "service"{
    lbvserver = citrixadc_lbvserver.lbvs.name
    name = format("%s-service", var.resource_prefix)
    ip = var.backend_service_ip
    servicetype  = "HTTP"
    port = 80

}

resource "citrixadc_cspolicy" "cspolicy"{
  csvserver       = citrixadc_csvserver.demo_csvserver.name
  targetlbvserver = citrixadc_lbvserver.lbvs.name
  policyname      = format("%s-cspolicy", var.resource_prefix)
  rule            = format("HTTP.REQ.HOSTNAME.SERVER.EQ(\"demo-bg.webapp.com\") && HTTP.REQ.URL.PATH.SET_TEXT_MODE(IGNORECASE).STARTSWITH(\"/\") && sys.random.mul(100).lt(%s)", var.traffic_weight)
  priority        = var.priority

  forcenew_id_set = [
    citrixadc_lbvserver.lbvs.id,
    citrixadc_csvserver.demo_csvserver.id,
  ]
}