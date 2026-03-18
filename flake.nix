{
  description = "Develop Python on Nix with uv";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
  };

  outputs =
    { nixpkgs, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          pythonEnvPkgs = with pkgs; [
            python314
            uv
            # Uncomment if necessary
            # pythonManylinuxPackages.manylinux2014Package
            # pythonManylinuxPackages.manylinux1
            # pythonManylinuxPackages.manylinux_x_y
          ];
          allPackages = pythonEnvPkgs;
          fhs = pkgs.buildFHSEnv {
            name = "py-uv-fhs";
            targetPkgs = pkgs: allPackages;
            profile = ''
              uv sync
              source .venv/bin/activate
            '';
          };
        in
        {
          default = fhs.env;
        }
      );
    };
}
