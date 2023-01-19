function decodeUplink(input) {
  var decoded = {};

  bytes=new Uint8Array([input.bytes[0],input.bytes[1],input.bytes[2],input.bytes[3]]);
  floatView=new Float32Array(bytes.buffer);
  decoded.lat=floatView[0];

  bytes=new Uint8Array([input.bytes[4],input.bytes[5],input.bytes[6],input.bytes[7]]);
  floatView=new Float32Array(bytes.buffer);
  decoded.lon=floatView[0];

  bytes=new Uint8Array([input.bytes[8],input.bytes[9],input.bytes[10],input.bytes[11]]);
  floatView=new Float32Array(bytes.buffer);
  decoded.alt=floatView[0];

  bytes=new Uint8Array([input.bytes[12],input.bytes[13],input.bytes[14],input.bytes[15]]);
  floatView=new Float32Array(bytes.buffer);
  decoded.course=floatView[0];

  bytes=new Uint8Array([input.bytes[16],input.bytes[17],input.bytes[18],input.bytes[19]]);
  floatView=new Float32Array(bytes.buffer);
  decoded.speed=floatView[0];

  bytes=new Uint8Array([input.bytes[24],input.bytes[25]]);
  dataView=new Int16Array(bytes.buffer);
  decoded.hdop=dataView[0];

  return {
    data: decoded
  };
}
