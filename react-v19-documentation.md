# React v19 - Latest Documentation Summary

## Overview
React v19 is now stable and available on npm! This document provides a comprehensive overview of the latest React features, improvements, and documentation based on the official React documentation from react.dev.

**Release Date**: December 5, 2024  
**Current Version**: React v19.1  
**Official Documentation**: https://react.dev

---

## 🆕 What's New in React 19

### 1. Actions
A revolutionary approach to handling data mutations with automatic pending states, error handling, and optimistic updates.

**Before Actions:**
```javascript
function UpdateName({}) {
  const [name, setName] = useState("");
  const [error, setError] = useState(null);
  const [isPending, setIsPending] = useState(false);

  const handleSubmit = async () => {
    setIsPending(true);
    const error = await updateName(name);
    setIsPending(false);
    if (error) {
      setError(error);
      return;
    } 
    redirect("/path");
  };

  return (
    <div>
      <input value={name} onChange={(event) => setName(event.target.value)} />
      <button onClick={handleSubmit} disabled={isPending}>
        Update
      </button>
      {error && <p>{error}</p>}
    </div>
  );
}
```

**With Actions:**
```javascript
function UpdateName({}) {
  const [name, setName] = useState("");
  const [error, setError] = useState(null);
  const [isPending, startTransition] = useTransition();

  const handleSubmit = () => {
    startTransition(async () => {
      const error = await updateName(name);
      if (error) {
        setError(error);
        return;
      } 
      redirect("/path");
    })
  };

  return (
    <div>
      <input value={name} onChange={(event) => setName(event.target.value)} />
      <button onClick={handleSubmit} disabled={isPending}>
        Update
      </button>
      {error && <p>{error}</p>}
    </div>
  );
}
```

### 2. New Hook: `useActionState`
Simplifies common Action patterns:

```javascript
const [error, submitAction, isPending] = useActionState(
  async (previousState, newName) => {
    const error = await updateName(newName);
    if (error) {
      return error;
    }
    // handle success
    return null;
  },
  null,
);
```

### 3. Form Actions
Native support for Actions in forms:

```javascript
function ChangeName({ name, setName }) {
  const [error, submitAction, isPending] = useActionState(
    async (previousState, formData) => {
      const error = await updateName(formData.get("name"));
      if (error) {
        return error;
      }
      redirect("/path");
      return null;
    },
    null,
  );

  return (
    <form action={submitAction}>
      <input type="text" name="name" />
      <button type="submit" disabled={isPending}>Update</button>
      {error && <p>{error}</p>}
    </form>
  );
}
```

### 4. New Hook: `useFormStatus`
Access form status without prop drilling:

```javascript
import {useFormStatus} from 'react-dom';

function DesignButton() {
  const {pending} = useFormStatus();
  return <button type="submit" disabled={pending} />
}
```

### 5. New Hook: `useOptimistic`
Handle optimistic updates easily:

```javascript
function ChangeName({currentName, onUpdateName}) {
  const [optimisticName, setOptimisticName] = useOptimistic(currentName);

  const submitAction = async formData => {
    const newName = formData.get("name");
    setOptimisticName(newName);
    const updatedName = await updateName(newName);
    onUpdateName(updatedName);
  };

  return (
    <form action={submitAction}>
      <p>Your name is: {optimisticName}</p>
      <p>
        <label>Change Name:</label>
        <input
          type="text"
          name="name"
          disabled={currentName !== optimisticName}
        />
      </p>
    </form>
  );
}
```

### 6. New API: `use`
Read resources in render:

```javascript
import {use} from 'react';

function Comments({commentsPromise}) {
  // `use` will suspend until the promise resolves.
  const comments = use(commentsPromise);
  return comments.map(comment => <p key={comment.id}>{comment}</p>);
}

function Page({commentsPromise}) {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Comments commentsPromise={commentsPromise} />
    </Suspense>
  )
}
```

**Reading Context with `use`:**
```javascript
import {use} from 'react';
import ThemeContext from './ThemeContext'

function Heading({children}) {
  if (children == null) {
    return null;
  }
  
  // This would not work with useContext
  // because of the early return.
  const theme = use(ThemeContext);
  return (
    <h1 style={{color: theme.color}}>
      {children}
    </h1>
  );
}
```

---

## 🏗️ New React DOM Static APIs

For static site generation:

```javascript
import { prerender } from 'react-dom/static';

async function handler(request) {
  const {prelude} = await prerender(<App />, {
    bootstrapScripts: ['/main.js']
  });
  return new Response(prelude, {
    headers: { 'content-type': 'text/html' },
  });
}
```

Available APIs:
- `prerender`
- `prerenderToNodeStream`

---

## 🚀 React Server Components

### Server Components
Components that render ahead of time, before bundling, in a separate environment from your client application.

### Server Actions
Allow Client Components to call async functions executed on the server:

```javascript
// Server Action (with "use server" directive)
async function updateUser(formData) {
  "use server";
  // Server-side logic
}

// Client Component
function UserForm() {
  return (
    <form action={updateUser}>
      <input name="name" />
      <button type="submit">Update</button>
    </form>
  );
}
```

---

## 🔧 Major Improvements in React 19

### 1. `ref` as a Prop
No more `forwardRef` needed:

```javascript
function MyInput({placeholder, ref}) {
  return <input placeholder={placeholder} ref={ref} />
}

// Usage
<MyInput ref={ref} />
```

### 2. Better Hydration Error Messages
Instead of multiple confusing errors, React 19 shows a single clear diff:

```
Uncaught Error: Hydration failed because the server rendered HTML didn't match the client.

<App>
  <span>
+   Client
-   Server
```

### 3. `<Context>` as a Provider
Simplified Context usage:

```javascript
const ThemeContext = createContext('');

function App({children}) {
  return (
    <ThemeContext value="dark">
      {children}
    </ThemeContext>
  );  
}
```

### 4. Cleanup Functions for Refs
```javascript
<input
  ref={(ref) => {
    // ref created

    // NEW: return a cleanup function
    return () => {
      // ref cleanup
    };
  }}
/>
```

### 5. `useDeferredValue` Initial Value
```javascript
function Search({deferredValue}) {
  // On initial render the value is ''.
  const value = useDeferredValue(deferredValue, '');
  
  return (
    <Results query={value} />
  );
}
```

### 6. Document Metadata Support
```javascript
function BlogPost({post}) {
  return (
    <article>
      <h1>{post.title}</h1>
      <title>{post.title}</title>
      <meta name="author" content="Josh" />
      <link rel="author" href="https://twitter.com/joshcstory/" />
      <meta name="keywords" content={post.keywords} />
      <p>
        Eee equals em-see-squared...
      </p>
    </article>
  );
}
```

### 7. Stylesheet Support
```javascript
function ComponentOne() {
  return (
    <Suspense fallback="loading...">
      <link rel="stylesheet" href="foo" precedence="default" />
      <link rel="stylesheet" href="bar" precedence="high" />
      <article class="foo-class bar-class">
        {...}
      </article>
    </Suspense>
  )
}
```

### 8. Async Script Support
```javascript
function MyComponent() {
  return (
    <div>
      <script async={true} src="..." />
      Hello World
    </div>
  )
}
```

### 9. Resource Preloading APIs
```javascript
import { prefetchDNS, preconnect, preload, preinit } from 'react-dom'

function MyComponent() {
  preinit('https://.../path/to/some/script.js', {as: 'script' })
  preload('https://.../path/to/font.woff', { as: 'font' })
  preload('https://.../path/to/stylesheet.css', { as: 'style' })
  prefetchDNS('https://...')
  preconnect('https://...')
}
```

### 10. Custom Elements Support
Full support for Custom Elements with proper property handling.

---

## 📚 Core React Concepts (Quick Start)

### Creating Components
```javascript
function MyButton() {
  return (
    <button>I'm a button</button>
  );
}

export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}
```

### JSX Rules
- Must close all tags: `<br />`
- Must wrap multiple elements in a parent or fragment: `<>...</>`
- Use `className` instead of `class`

### Displaying Data
```javascript
const user = {
  name: 'Hedy Lamarr',
  imageUrl: 'https://i.imgur.com/yXOvdOSs.jpg',
  imageSize: 90,
};

export default function Profile() {
  return (
    <>
      <h1>{user.name}</h1>
      <img
        className="avatar"
        src={user.imageUrl}
        alt={'Photo of ' + user.name}
        style={{
          width: user.imageSize,
          height: user.imageSize
        }}
      />
    </>
  );
}
```

### Conditional Rendering
```javascript
// Using if statement
let content;
if (isLoggedIn) {
  content = <AdminPanel />;
} else {
  content = <LoginForm />;
}

// Using ternary operator
<div>
  {isLoggedIn ? (
    <AdminPanel />
  ) : (
    <LoginForm />
  )}
</div>

// Using logical AND
<div>
  {isLoggedIn && <AdminPanel />}
</div>
```

### Rendering Lists
```javascript
const products = [
  { title: 'Cabbage', id: 1 },
  { title: 'Garlic', id: 2 },
  { title: 'Apple', id: 3 },
];

const listItems = products.map(product =>
  <li key={product.id}>
    {product.title}
  </li>
);

return <ul>{listItems}</ul>;
```

### Event Handling
```javascript
function MyButton() {
  function handleClick() {
    alert('You clicked me!');
  }

  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}
```

### State Management
```javascript
import { useState } from 'react';

function MyButton() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <button onClick={handleClick}>
      Clicked {count} times
    </button>
  );
}
```

### Sharing State Between Components
```javascript
import { useState } from 'react';

export default function MyApp() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <div>
      <h1>Counters that update together</h1>
      <MyButton count={count} onClick={handleClick} />
      <MyButton count={count} onClick={handleClick} />
    </div>
  );
}

function MyButton({ count, onClick }) {
  return (
    <button onClick={onClick}>
      Clicked {count} times
    </button>
  );
}
```

---

## 🔗 Key Resources

- **Official Documentation**: https://react.dev
- **React v19 Release Notes**: https://react.dev/blog/2024/12/05/react-19
- **Upgrade Guide**: https://react.dev/blog/2024/04/25/react-19-upgrade-guide
- **API Reference**: https://react.dev/reference/react
- **React DOM APIs**: https://react.dev/reference/react-dom
- **Tutorial**: https://react.dev/learn/tutorial-tic-tac-toe

---

## 📝 Migration Notes

- React 19 includes breaking changes - see the upgrade guide
- `forwardRef` will be deprecated in future versions
- `<Context.Provider>` will be deprecated in favor of `<Context>`
- New error handling with `onCaughtError`, `onUncaughtError`, and `onRecoverableError`

This documentation reflects the latest stable React v19 release as of December 2024.
