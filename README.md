
## HAG network link policy (2026-09-30)

Run `python3 scripts/hag_link_policy.py <this-site-host>` after any chrome/nav rebuild, translation run or new page. It is idempotent and:
- tags every link to xshielder.com `rel="sponsored"` with UTM (`utm_campaign=hag_network`),
- adds `nofollow` to competitor links (list in the script),
- removes links to the other network sites from header/nav/footer (links in the text stay followed),
- inserts the footer sponsor line ("This site's main sponsor is Xshielder. Want to sponsor this site? Contact us. Part of the Hazardous Area Guide network.") in the page language,
- adds sponsored in-text callouts on the pages listed in `CALLOUTS`,
- loads `hag-links.js`, which sends a GA4 `network_link_click` event (link_type, placement) for every outbound click.
