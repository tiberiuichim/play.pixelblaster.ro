+++
Categories = ["Volto", "Plone"]
Description = ""
Tags = ["cookbook","Plone", "Volto"]
date = "2022-07-18T17:10:16+03:00"
menu = "main"
title = "Volto recipe for footer actions managed as site content"

+++

Managing the Footer as content is one of the common tasks on a Plone / Volto
website. One typical approach is to designate some root folder, let's say
`footer-links` as a container for Link instances, and use those links as
shortcuts to dedicated pages.

So, a footer component may look like this:


```jsx
import React from 'react';
import { getContent } from '@plone/volto/actions';
import { useSelector } from 'react-redux';
import {UniversalLink} from '@plone/volto/components';

const Footer = () => {

  const footerLinks = useSelector((state) => state.content.subrequests?.footer?.data?.items || []);

  React.useEffect(() => {
    getContent('/footer-links', null, 'footer');
  }, []);

  return footerLinks.map((item) =>
    <UniversalLink item={item} key={item['@id']}>{item.title}</UniversalLink>)
}
```

This approach works, but it's a bit naive. There may be unneeded network
requests and, most important, the content of this footer is not included in the
server-side rendered HTML.

If you're willing to write some Python code, this may be a relatively
straight-forward fix: write some expander that automatically inserts the links
as a `@component` in the current content response, so it can be picked up by
the Footer component.

There is a solution for this problem, in case we want to keep things pure
frontend-level. Volto provides an extension mechanism for its SSR framework,
the `config.settings.asyncPropsExtenders`.

Here's how I did it for a multilingual website:

```jsx
  config.settings.asyncPropsExtenders = [
    ...(config.settings.asyncPropsExtenders || []),
    {
      path: '/',
      extend: (dispatchActions) => {
        const action = {
          key: 'footer',
          promise: ({ location, store }) => {
            // const currentLang = state.intl.locale;
            const bits = location.pathname.split('/');
            const currentLang =
              bits.length >= 2 ? bits[1] || DEFAULT_LANG : DEFAULT_LANG;

            const state = store.getState();
            if (state.content.subrequests?.[`footer-${currentLang}`]?.data) {
              return;
            }

            const url = `/${currentLang}/footer-links`;
            const action = getContent(url, null, `footer-${currentLang}`);
            return store.dispatch(action).catch((e) => {
              // eslint-disable-next-line
              console.log(
                `Footer links folder not found: ${url}. Please create as folder
                named footer-links in the root of your current language`,
              );
            });
          },
        };
        return [...dispatchActions, action];
      },
    },
  ];
```

And my Footer component is now simply:

```jsx
function Footer(props) {
  const currentLang = useSelector((state) => state.intl.locale);
  const footerLinks = useSelector(
    (state) =>
      state.content.subrequests?.[`footer-${currentLang}`]?.data?.items || [],
  );

  return footerLinks.map((item, i) => (
    <UniversalLink key={`${item.id}-${i}`} item={item}>
      {item.title}
    </UniversalLink>
  ));
}
```
