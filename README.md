# helix_service_kenan

To run it locally:

```
git clone
make devsetup
make up
```

Then navigate to: http://localhost:5000/graphql

1. Simple query

```graphql
query getProviders {
    providers(
        query_id: "foo"
    ) {
        total_count
        results {
            result_id
        }
    }
}

```

## Writing end-to-end tests

1. Right-click the "end_to_end" folder in Pycharm and choose New "End to End Test"
2. Type in name of the test
3. Create a graphql folder and create a query.gql file in there and paste in the graphql query (You can get this from
   the PSS graphql testing UI: `https://provider-search.dev.bwell.zone/graphql`)
4. Create an expected folder and store a .json file in there with what you expect as the result.  (You can start with an
   existing result from PSS and edit it to be what you expect)
5. That's it. Now when you run the test, it will create an index, run your graphql query and compare the result with
   your expected result

You can look at existing end-to-end tests for more info.

#### Multi scenario end to end tests

The test framework supports testing multiple scenarios per end to end test. This is done by adding files to the graphql
and expected directories that have the same name. This is helpful when you want to test
multiple test cases. For example testing filtering by distance using multiple values for distance,
[that example is here](https://github.com/icanbwell/helix.providersearch/tree/main/tests/end_to_end/test_filter_by_distance)
.



