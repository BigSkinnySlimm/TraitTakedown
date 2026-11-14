class StudioNetworkBroker {
  constructor(callsign) {
    this.callsign = callsign;
  }
  setCallsign(name) {
    this.callsign = String(name || "Commander").replace(/[^a-zA-Z0-9_-]/g, "").slice(0, 16) || "Commander";
    return this.callsign;
  }
}
window.StudioNetworkBroker = StudioNetworkBroker;
