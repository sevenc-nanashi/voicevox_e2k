export abstract class SourceProvider {
  abstract getWords(): Promise<string[]>;
}
