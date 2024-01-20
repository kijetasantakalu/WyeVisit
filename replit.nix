{ pkgs }: {
  deps = [
    pkgs.cmakeMinimal
    pkgs.cmake
    pkgs.hol
    pkgs.wget
    pkgs.sqlite.bin
    pkgs.python38Full
  ];
  env = {
    PYTHONBIN = "${pkgs.python38Full}/bin/python3.8";
    LANG = "en_US.UTF-8";
  };
}