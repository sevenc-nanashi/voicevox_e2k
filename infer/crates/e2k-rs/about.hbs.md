<!-- `task build` にて生成。手動で編集しないでください。 -->
# Rust Licenses

e2k-rs が依存しているクレートのライセンス一覧です。

{{#each overview}}
- {{name}} ({{count}})
{{/each}}


---

{{ #each licenses }}
## {{ name }}

{{ #each used_by }}
{{ #if crate.repository }}
- [{{crate.name}}]({{crate.repository}})
{{ else }}
- [{{crate.name}}](https://crates.io/crates/{{crate.name}})
{{ /if }}
{{ /each }}

```
{{{ text }}}
```
{{ /each }}
