class StudioNetworkBroker {
  constructor(callsign, callbacks) {
    this.callsign = callsign;
    this.cb = callbacks;
    this.peer = null;
    this.conn = null;
    this.initPeer();
  }

  clean(id) {
    return String(id || "Commander").replace(/[^a-zA-Z0-9_-]/g, "").slice(0, 16) || "Commander";
  }

  peerId(name) {
    return "tt-v9-user-" + this.clean(name).toLowerCase();
  }

  initPeer() {
    if (typeof Peer === "undefined") return;
    try {
      if (this.peer) this.peer.destroy();
      this.peer = new Peer(this.peerId(this.callsign), { debug: 0 });
      this.peer.on("open", () => this.cb.onOnline(this.callsign));
      this.peer.on("connection", (c) => {
        c.on("open", () => {
          c.on("data", (msg) => {
            if (msg.type === "DIRECT_CHALLENGE") {
              this.cb.onChallenge(msg.from, c);
            } else {
              this.cb.onData(msg);
            }
          });
        });
      });
    } catch (e) {}
  }

  setCallsign(name) {
    this.callsign = this.clean(name);
    this.initPeer();
    return this.callsign;
  }

  challengeFriend(friendName) {
    if (!this.peer) return false;
    const c = this.peer.connect(this.peerId(friendName), { reliable: true });
    c.on("open", () => {
      this.conn = c;
      c.send({ type: "DIRECT_CHALLENGE", from: this.callsign });
    });
    return true;
  }
}

window.StudioNetworkBroker = StudioNetworkBroker;
