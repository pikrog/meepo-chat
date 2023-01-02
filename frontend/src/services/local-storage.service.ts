type LocalStorageKeys = 'access_token' | 'server_address';

export function setInLocalStorage(key: LocalStorageKeys, value: string) {
  window.localStorage.setItem(key, value);
}

export function getFromLocalStorage(key: LocalStorageKeys) {
  return window.localStorage.getItem(key);
}