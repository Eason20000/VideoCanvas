{
  description = "VideoCanvas";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs =
    { self, nixpkgs, ... }:
    let
      system = "x86_64-linux";
    in
    {
      devShells."${system}".default =
        let
          pkgs = import nixpkgs { inherit system; };
          base = pkgs.appimageTools.defaultFhsEnvArgs;
        in
        pkgs.mkShell {
          packages = [
            (pkgs.buildFHSEnv (
              base
              // {
                name = "fhs";
                targetPkgs = pkgs: (base.targetPkgs pkgs) ++ (with pkgs; [ uv ]);
                runScript = "bash";
              }
            ))
          ];
          shellHook = ''
            fhs
            exit
          '';
        };
    };

}
