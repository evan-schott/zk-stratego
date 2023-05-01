# aleo-sdk

This is an unofficial fork of [AleoHQ/aleo](https://github.com/AleoHQ/aleo)

## Publish instructions

```bash
npm login
wasm-pack build --target web
cp template.package.json pkg/package.json
cd pkg
npm publish --access=public
```
